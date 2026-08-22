"""Focused test: composite a slide, refine via Gemini, remove watermark.

Opens browser for Gemini login if needed, then runs the refinement.
"""

import asyncio
import sys
import os
import urllib.request
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from loguru import logger

logger.remove()
logger.add(sys.stderr, level="DEBUG",
           format="<green>{time:HH:mm:ss}</green> | <level>{level:<8}</level> | {message}")


async def test_refine():
    from src.generator.brand_compositor import composite_slide
    from src.generator.image_refiner import refine_slide, remove_watermark
    from src.browser.gemini import GeminiClient

    test_dir = PROJECT_ROOT / "data" / "media" / "test_refine"
    test_dir.mkdir(parents=True, exist_ok=True)

    # ── Step 1: Download YouTube thumbnail ──
    video_id = "e_v7btvJfKY"
    thumb_path = test_dir / "test_thumb.jpg"
    if not thumb_path.exists():
        logger.info("Downloading YouTube thumbnail...")
        for quality in ["maxresdefault", "hqdefault", "mqdefault"]:
            url = f"https://img.youtube.com/vi/{video_id}/{quality}.jpg"
            try:
                urllib.request.urlretrieve(url, str(thumb_path))
                if thumb_path.stat().st_size > 5000:
                    logger.info(f"Thumbnail downloaded: {quality}")
                    break
            except Exception:
                continue

    if not thumb_path.exists():
        logger.error("Could not download thumbnail!")
        return

    # ── Step 2: Composite slide ──
    logger.info("Compositing slide with Pillow...")
    composited_path = str(test_dir / "01_composited.png")
    composite_slide(
        background_path=str(thumb_path),
        headline="Ali Ka White Kurta Tabah",
        body_text="Ali Ne Socha Nahi Hoga Late Ana Itna Mehnga Parega. Abubakar Ne Revenge Liya.",
        output_path=composited_path,
        slide_number=1,
        total_slides=4,
        highlight_words=["Abubakar"],
    )
    logger.info(f"Composited: {composited_path}")

    # ── Step 3: Connect to Gemini (let user login if needed) ──
    logger.info("Opening Gemini browser — login if prompted...")
    gemini = GeminiClient()
    try:
        await gemini.connect(headless=False)
    except RuntimeError as e:
        logger.warning(f"Gemini not logged in: {e}")
        logger.info("Please log into Gemini in the browser window, then press Enter here...")
        await asyncio.get_event_loop().run_in_executor(None, input)
        # Retry after manual login
        await gemini._page.goto("https://gemini.google.com/app", wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(5)
        logger.info("Retrying after login...")

    # ── Step 4: Refine via Gemini ──
    logger.info("Sending to Gemini for refinement...")
    refined_path = str(test_dir / "02_refined.png")
    result = await refine_slide(gemini, composited_path, refined_path)

    if result:
        logger.info(f"REFINED: {result}")
    else:
        logger.warning("Refinement failed — check Gemini browser window for errors")

    await gemini.close()

    # ── Summary ──
    logger.info(f"\n{'='*50}")
    logger.info("TEST COMPLETE")
    logger.info(f"  Composited: {composited_path}")
    if result:
        logger.info(f"  Refined:    {result}")
    logger.info(f"{'='*50}")

    os.startfile(str(test_dir))


if __name__ == "__main__":
    asyncio.run(test_refine())
