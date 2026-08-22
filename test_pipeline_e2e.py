"""End-to-end pipeline test — runs one video through the full flow.

Stops BEFORE publishing so you can inspect:
  1. Analysis output (what the AI understood)
  2. Generated slide images (visual consistency)
  3. Caption text (Roman Urdu + English quality)
  4. Hashtags

Opens the output folder when done.
"""

import asyncio
import json
import sys
import os
from pathlib import Path

# Ensure project root on path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from loguru import logger

# Setup logging to console
logger.remove()
logger.add(sys.stderr, level="INFO",
           format="<green>{time:HH:mm:ss}</green> | <level>{level:<8}</level> | {message}")


async def run_test(video_db_id: int = None):
    """Run the full pipeline on one video, stop before publish."""
    from src.database.engine import init_db, SessionLocal
    from src.database.models import Video, GeneratedContent

    init_db()
    db = SessionLocal()

    try:
        # Pick the video
        if video_db_id:
            video = db.query(Video).get(video_db_id)
        else:
            # Pick first detected video
            video = db.query(Video).filter(Video.status == "detected").first()

        if not video:
            logger.error("No video found to test!")
            return

        logger.info(f"{'='*60}")
        logger.info(f"TESTING PIPELINE: {video.title}")
        logger.info(f"Video ID: {video.video_id}")
        logger.info(f"URL: {video.url}")
        logger.info(f"Current status: {video.status}")
        logger.info(f"{'='*60}")

        # Import pipeline
        from src.pipeline import (
            analyze_video, generate_pipeline_images,
            generate_caption, generate_hashtags,
            get_video_content_dir,
        )
        from src.browser.youtube_ask import YouTubeAskClient
        from src.browser.gemini import GeminiClient

        content_dir = get_video_content_dir(video.video_id, video.title)
        logger.info(f"Output directory: {content_dir}")

        # ── Step 1: Analysis ──
        logger.info(f"\n{'─'*40}")
        logger.info("STEP 1: Analyzing video...")
        logger.info(f"{'─'*40}")

        yt_client = YouTubeAskClient()
        await yt_client.connect(headless=False)

        gemini = GeminiClient()
        await gemini.connect(headless=False)

        analysis = await analyze_video(db, video, yt_client, gemini)
        if not analysis:
            logger.error("Analysis failed! Cannot continue.")
            await yt_client.close()
            await gemini.close()
            return

        # Save analysis to a readable file
        analysis_file = content_dir / "analysis_output.json"
        with open(analysis_file, "w", encoding="utf-8") as f:
            safe = {k: v for k, v in analysis.items() if k != "_raw_response"}
            json.dump(safe, f, indent=2, ensure_ascii=False)
        logger.info(f"Analysis saved to: {analysis_file}")

        # Print key analysis results
        logger.info(f"  Summary: {analysis.get('summary', 'N/A')[:100]}")
        logger.info(f"  Category: {analysis.get('content_category', 'N/A')}")
        logger.info(f"  Controversy: {analysis.get('controversy_level', 'N/A')}/10")
        logger.info(f"  Newsworthiness: {analysis.get('newsworthiness', 'N/A')}/10")
        logger.info(f"  Post type: {analysis.get('recommended_post_type', 'N/A')}")
        logger.info(f"  Key facts: {len(analysis.get('key_facts', []))}")
        logger.info(f"  Hook: {analysis.get('suggested_caption_hook', 'N/A')[:80]}")

        # ── Step 2: Caption ──
        logger.info(f"\n{'─'*40}")
        logger.info("STEP 2: Generating caption...")
        logger.info(f"{'─'*40}")

        caption = await generate_caption(db, analysis, gemini)
        caption_file = content_dir / "caption.txt"
        with open(caption_file, "w", encoding="utf-8") as f:
            f.write(caption)
        logger.info(f"Caption saved to: {caption_file}")
        logger.info(f"Caption preview: {caption[:150]}...")

        # ── Step 3: Hashtags ──
        logger.info(f"\n{'─'*40}")
        logger.info("STEP 3: Generating hashtags...")
        logger.info(f"{'─'*40}")

        hashtags = await generate_hashtags(db, analysis, gemini)
        hashtags_file = content_dir / "hashtags.txt"
        with open(hashtags_file, "w", encoding="utf-8") as f:
            f.write(" ".join(hashtags))
        logger.info(f"Hashtags: {' '.join(hashtags)}")

        # ── Step 4: Images ──
        logger.info(f"\n{'─'*40}")
        logger.info("STEP 4: Generating slide images...")
        logger.info(f"{'─'*40}")

        image_paths = await generate_pipeline_images(db, video, analysis, gemini)
        logger.info(f"Generated {len(image_paths)} slide(s)")
        for i, p in enumerate(image_paths, 1):
            logger.info(f"  Slide {i}: {p}")

        # ── Step 5: Reel Video ──
        video_path = ""
        if len(image_paths) > 1:
            logger.info(f"\n{'─'*40}")
            logger.info("STEP 5: Generating reel video with music...")
            logger.info(f"{'─'*40}")

            from src.pipeline import _create_reel_video_async
            video_path = await _create_reel_video_async(video, image_paths, caption, analysis, gemini)
            if video_path:
                logger.info(f"Reel video created: {video_path}")
            else:
                logger.warning("Reel video creation failed or returned empty")
        else:
            logger.info("\nSkipping reel video (single image, not carousel)")

        # ── Save content to DB ──
        from src.database.crud import create_generated_content, update_video_status
        all_media = image_paths + ([video_path] if video_path else [])
        content = create_generated_content(
            db, video.id,
            post_type="carousel" if len(image_paths) > 1 else "image",
            caption=caption,
            hashtags=hashtags,
            media_paths=all_media,
        )
        update_video_status(db, video.id, "content_generated")
        logger.info(f"Content saved to DB as #{content.id}")

        # ── Summary ──
        logger.info(f"\n{'='*60}")
        logger.info("PIPELINE TEST COMPLETE")
        logger.info(f"{'='*60}")
        logger.info(f"Output folder: {content_dir}")
        logger.info(f"Slides generated: {len(image_paths)}")
        logger.info(f"Reel video: {'YES' if video_path else 'NO'}")
        logger.info(f"Caption length: {len(caption)} chars")
        logger.info(f"Hashtags: {len(hashtags)}")
        logger.info(f"Status: content_generated (NOT published)")
        logger.info(f"")
        logger.info(f"Check these files for consistency:")
        logger.info(f"  {content_dir / 'slides'}")
        logger.info(f"  {content_dir / 'caption.txt'}")
        logger.info(f"  {content_dir / 'hashtags.txt'}")
        logger.info(f"  {content_dir / 'analysis_output.json'}")
        if video_path:
            logger.info(f"  {video_path}")

        # Open the output folder
        os.startfile(str(content_dir))

        await yt_client.close()
        await gemini.close()

    finally:
        db.close()


if __name__ == "__main__":
    # Default: video #28 (Arsalan Naseer), or pass ID as argument
    vid_id = int(sys.argv[1]) if len(sys.argv) > 1 else 28
    asyncio.run(run_test(vid_id))
