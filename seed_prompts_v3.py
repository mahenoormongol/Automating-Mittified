"""Seed v3 meta-context engineered prompts into the database.

Run: python seed_prompts_v3.py

This deactivates all existing prompts and inserts v3 structured prompts
with design system integration for pixel-perfect consistent output.
"""

from src.database.engine import SessionLocal, init_db
from src.database.models import PromptTemplate
from config.prompts.image_gen import MITTIFIED_DESIGN_SYSTEM

init_db()
db = SessionLocal()

# ── Deactivate all existing prompts ─────────────────────────────────────
db.query(PromptTemplate).update({"is_active": False})
db.commit()
print("Deactivated all existing prompts.")

# ── v3 Prompt Definitions ───────────────────────────────────────────────

V3_PROMPTS = [
    # ── 1. VIDEO ANALYSIS (YouTube Ask / Gemini) ────────────────────────
    {
        "name": "Video Analysis (Meta-Context v3)",
        "category": "video_analysis",
        "version": 3,
        "template": """Analyze this video for the MITTIFIED Instagram content pipeline.

<CONTEXT>
You are MITTIFIED's content analyst — expert in Pakistani entertainment, drama industry, and celebrity news.
Your output feeds an automated system that generates Instagram carousel posts.
Downstream systems need: key_facts with timestamps (for YouTube screenshot capture), sentiment (for image mood), people names (for hashtags), and a Roman Urdu hook line (for the slide headline).
Your response is parsed by json.loads() — it MUST be valid JSON with zero errors.
</CONTEXT>

<OUTPUT_SCHEMA>
Respond with EXACTLY this JSON structure. Every field is required:

{{
  "summary": "2-3 sentence summary in English. Be specific — name people, dramas, channels.",
  "key_topics": ["specific topic 1", "specific topic 2", "specific topic 3"],
  "people_mentioned": ["Full Name 1", "Full Name 2"],
  "drama_names": ["Drama Name 1"],
  "sentiment": "positive|negative|neutral|mixed",
  "emotional_tone": "serious|humorous|angry|sad|excited|informative",
  "controversy_level": 5,
  "newsworthiness": 7,
  "content_category": "drama_review|celebrity_news|industry_news|controversy|behind_scenes|ratings|awards|other",
  "key_facts": [
    {{
      "fact": "One specific claim/event from the video. Concrete, not vague.",
      "timestamp": "m:ss",
      "visual_description": "What is visually shown on screen at this moment."
    }}
  ],
  "suggested_caption_hook": "Roman Urdu + English hook. Example: 'Feroze Khan ne sab ko chonka dia!'",
  "recommended_post_type": "carousel",
  "recommended_slides": 4,
  "why_post_type": "Brief reason."
}}
</OUTPUT_SCHEMA>

<RULES>
  • key_facts MUST have 3-10 entries, each with a valid timestamp in m:ss format
  • controversy_level and newsworthiness are integers 1-10
  • If video > 2 minutes → recommended_post_type MUST be "carousel"
  • suggested_caption_hook MUST be Roman Urdu + English (like Pakistani youth texting)
  • Use full names: "Feroze Khan" not "FK", "Iqra Aziz" not "Iqra"
  • Pakistani TV channels: HUM TV, ARY Digital, Geo TV, Green TV, Express TV
  • NO markdown, NO code blocks, NO commentary outside the JSON
</RULES>""",
    },

    # ── 2. IMAGE GENERATION — HOOK SLIDE ────────────────────────────────
    {
        "name": "Hook Slide (Meta-Context v3)",
        "category": "image_generation",
        "version": 3,
        "template": f"""Generate the HOOK SLIDE (Slide 1) — the most important slide that stops the scroll.

<SYSTEM_CONTEXT>
You are generating an Instagram carousel slide image for MITTIFIED, a Pakistani entertainment news brand.
This is Slide {{slide_number}} of {{total_slides}}.
The hook slide is the FIRST thing people see — it must be dramatic, bold, and information-rich.
</SYSTEM_CONTEXT>

{MITTIFIED_DESIGN_SYSTEM}

<THIS_SLIDE_CONTENT>
Video Title: {{title}}
Topic: {{topic}}
Summary: {{summary}}
People Involved: {{people}}
Category: {{category}}
Mood/Sentiment: {{sentiment}}
Hook Headline (display this as the gold #D4A030 headline): {{headline}}
</THIS_SLIDE_CONTENT>

<GENERATION_INSTRUCTIONS>
Generate a 1080×1350 portrait image following the design system EXACTLY:

1. BACKGROUND: A dramatic, cinematic visual relevant to the topic.
   Use dark, moody tones. No real human faces. No YouTube UI.

2. GRADIENT VEIL: Dark gradient covering bottom 45% for text readability.

3. BRAND BADGE: "MITTIFIED" wordmark + shield icon, top-left, white, 32px from edges.
   @Mittified handle below it with checkmark.

4. HEADLINE TEXT: Display "{{headline}}" in bold amber gold (#D4A030).
   Position in the bottom 35%. Left-aligned. Max 2 lines.
   MUST be Roman Urdu + English mix. NOT English-only.

5. BODY TEXT: A 1-2 line supporting detail in white (#FFFFFF).
   Highlight 1-2 key names/phrases in bright amber (#F6B929).

6. FOOTER BAR: Dark strip (#111111) at very bottom.
   Left: "FOLLOW" label. Right: "Swipe Left for Next →"

CRITICAL: The output image must be EXACTLY 1080×1350 pixels, portrait orientation.
</GENERATION_INSTRUCTIONS>""",
    },

    # ── 3. DETAIL SLIDE ─────────────────────────────────────────────────
    {
        "name": "Detail Slide (Meta-Context v3)",
        "category": "detail_slide",
        "version": 3,
        "template": f"""Generate a DETAIL SLIDE (Slide {{slide_number}} of {{total_slides}}) for the carousel.

<SYSTEM_CONTEXT>
This is a continuation slide in a MITTIFIED Instagram carousel.
It MUST be visually IDENTICAL in layout, dimensions, and style to Slide 1.
The ONLY difference is the headline text and body text content.
If someone placed all slides side by side, they must look like one cohesive set.
</SYSTEM_CONTEXT>

{MITTIFIED_DESIGN_SYSTEM}

<THIS_SLIDE_CONTENT>
Slide: {{slide_number}} of {{total_slides}}
Overall Topic: {{topic}}
Video Title: {{title}}

THIS SLIDE'S KEY POINT (use as headline):
"{{fact}}"
</THIS_SLIDE_CONTENT>

<GENERATION_INSTRUCTIONS>
Generate a 1080×1350 portrait image with IDENTICAL layout to Slide 1:

1. BACKGROUND: A different dramatic visual from Slide 1, but SAME mood/tone.
   Still dark, cinematic. No real faces. No YouTube UI.

2. GRADIENT VEIL: Same gradient as Slide 1. Bottom 45% darkened.

3. BRAND BADGE: SAME position, SAME size, SAME style as Slide 1.
   "MITTIFIED" + @Mittified, top-left, white.

4. HEADLINE TEXT: Rephrase "{{fact}}" into a catchy Roman Urdu + English headline.
   SAME position as Slide 1's headline. SAME amber gold (#D4A030). SAME font size.
   DO NOT use the English fact text verbatim — translate the meaning into Roman Urdu style.
   Example: If fact is "Court hearing on April 8" → headline is "Court Ka Faisla April 8 Ko!"

5. BODY TEXT: 1-2 lines expanding on this specific point. White (#FFFFFF).
   Highlight key name/phrase in bright amber (#F6B929).

6. FOOTER BAR: SAME as Slide 1. Dark strip, "Swipe Left for Next →"

STYLE CONSISTENCY CHECK:
  ☐ Same 1080×1350 dimensions as Slide 1?
  ☐ Same gradient darkness and position?
  ☐ Same brand badge position and size?
  ☐ Same headline color (#D4A030) and approximate size?
  ☐ Same body text color (#FFFFFF) and position?
  ☐ Same footer bar style?
  → If any checkbox is NO, fix it before outputting.
</GENERATION_INSTRUCTIONS>""",
    },

    # ── 4. BACKGROUND OVERLAY (SHOT 2) ──────────────────────────────────
    {
        "name": "Background Overlay Shot 2 (Meta-Context v3)",
        "category": "background_overlay",
        "version": 3,
        "template": """Take the YouTube screenshot I just uploaded and composite it as the BACKGROUND of the Instagram slide you generated above.

<SYSTEM_CONTEXT>
This is the SECOND shot in a two-shot workflow:
  Shot 1: You generated an Instagram slide with a generic/AI background
  Shot 2 (NOW): Replace that generic background with the REAL scene from the YouTube video

The attached image is a raw YouTube screenshot. It contains the actual video frame
PLUS YouTube player UI (play button, progress bar, etc.) that MUST be removed.
</SYSTEM_CONTEXT>

<EXTRACTION_RULES>
From the YouTube screenshot, extract ONLY:
  ✓ The actual video content (people, scenes, objects, settings)
  ✓ The colors, lighting, and mood of the scene
  ✗ REMOVE: Play/pause button overlay
  ✗ REMOVE: Red progress bar / scrubber
  ✗ REMOVE: Time display (0:00 / 5:32)
  ✗ REMOVE: Volume, settings, fullscreen icons
  ✗ REMOVE: Video title bar
  ✗ REMOVE: Browser chrome, search bar, tabs
  ✗ REMOVE: Any YouTube branding (logo, red elements)
  ✗ REMOVE: Any "Ad" overlays or banners
</EXTRACTION_RULES>

<COMPOSITING_RULES>
1. Place the extracted video scene as Layer 1 (BACKGROUND) — full bleed, edge to edge
2. KEEP the gradient veil from the slide above (dark overlay on bottom 45%)
   If the scene is bright, INCREASE the gradient opacity so text remains readable
3. KEEP ALL text exactly as generated in Shot 1:
   - MITTIFIED brand badge (top-left) — do not move, resize, or remove
   - Headline text (gold #D4A030) — do not change text, color, or position
   - Body text (white #FFFFFF) — do not change text, color, or position
   - Footer bar (#111111) — do not change
4. The final image must look like a PROFESSIONALLY DESIGNED Instagram post
   with a real photograph as background — NOT like a screenshot was pasted behind text
5. Blend naturally: match the scene's lighting with the overlay
6. Output dimensions: EXACTLY the same as Shot 1 (1080×1350)
</COMPOSITING_RULES>

<QUALITY_GATE>
The output passes ONLY if:
  ☐ Zero YouTube UI elements visible
  ☐ All text from Shot 1 is intact and readable
  ☐ MITTIFIED brand badge is in the exact same position
  ☐ Background feels natural, not pasted-on
  ☐ Dimensions are identical to Shot 1
</QUALITY_GATE>""",
    },

    # ── 5. CAPTION WRITER ───────────────────────────────────────────────
    {
        "name": "Caption Writer (Meta-Context v3)",
        "category": "caption",
        "version": 3,
        "template": """You are the voice of MITTIFIED — a Pakistani entertainment Instagram page by and for young Pakistanis.

<CONTEXT>
Platform: Instagram caption (appears below carousel/image post)
Audience: Pakistani youth 18-35, Urdu-speaking, Instagram-native
Voice: You talk EXACTLY like a Pakistani friend sharing gossip in a WhatsApp group
Language: Roman Urdu + English mix — NON-NEGOTIABLE
  ✓ "Yaar ye toh bohat shocking hai! ARY ne kamaal kar dia 🔥"
  ✗ "This is truly shocking! ARY has done something amazing."
  ✗ "یہ بہت حیران کن ہے" (no Urdu script — Roman only)
</CONTEXT>

<INPUT>
{analysis}
</INPUT>

<OUTPUT_STRUCTURE>
LINE 1 — HOOK (scroll-stopper):
  Bold, dramatic. Creates urgency or curiosity.
  Patterns: "BREAKING: [claim] 🔥" | "[Name] ne chonka dia! 😱" | "Ye kya ho raha hai? 👀"

LINES 2-5 — BODY:
  Specific details: drama names, actor names, channel names.
  Short paragraphs with line breaks. 1-2 emojis per paragraph max.

LAST LINE — CTA:
  Question or call-to-action for comments.
  "Tumhara kya khayal hai? Comment mein btao! 👇"

RULES:
  • 150-400 words
  • NO hashtags (system adds them)
  • NO "Caption:" prefix
  • NO Urdu script — Roman Urdu ONLY
  • Be opinionated and spicy
  • Reference specific names/shows/events
</OUTPUT_STRUCTURE>

Write ONLY the caption:""",
    },

    # ── 6. HASHTAG GENERATOR ────────────────────────────────────────────
    {
        "name": "Hashtag Generator (Meta-Context v3)",
        "category": "hashtags",
        "version": 3,
        "template": """Generate targeted Instagram hashtags for a MITTIFIED post.

<CONTEXT>
Instagram 2025: Algorithm favors 5-8 specific hashtags over 30 spammy ones.
Brand: MITTIFIED — Pakistani entertainment/drama news
Mix English + Roman Urdu hashtags for the Pakistani audience.
</CONTEXT>

<INPUT>
Topic: {topic}
People: {people}
Category: {category}
</INPUT>

<OUTPUT_CONTRACT>
Return a JSON array of {count} hashtags. NOTHING else — no explanation, no markdown.

DISTRIBUTION ORDER:
  1. #Mittified (ALWAYS first)
  2. 2-3 person/drama-specific (#FerozeKhan, #TereBin, #ARYDigital)
  3. 2-3 category tags (#PakistaniDrama, #DramaReview, #CelebrityNews)
  4. 1-2 broad reach (#Pakistan, #Trending, #Viral)
  5. 1 Roman Urdu tag if natural (#NayiKhabar, #DramaUpdate, #BreakingNews)

RULES:
  • CamelCase (#PakistaniDrama not #pakistanidrama)
  • NO generic spam (#love, #instagood, #photooftheday)
  • Every tag must be relevant to THIS specific post
</OUTPUT_CONTRACT>

JSON array:""",
    },
]

# ── Insert all v3 prompts ───────────────────────────────────────────────

for prompt_data in V3_PROMPTS:
    tpl = PromptTemplate(
        name=prompt_data["name"],
        category=prompt_data["category"],
        version=prompt_data["version"],
        template=prompt_data["template"],
        is_active=True,
    )
    db.add(tpl)
    print(f"  + {prompt_data['name']} (category={prompt_data['category']}, v{prompt_data['version']})")

db.commit()
db.close()

print(f"\nDone! {len(V3_PROMPTS)} v3 meta-context prompts seeded.")
print("Old prompts deactivated (still in DB for rollback if needed).")
