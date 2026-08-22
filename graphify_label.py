import sys, json
from graphify.build import build_from_json
from graphify.cluster import score_all
from graphify.analyze import god_nodes, surprising_connections, suggest_questions
from graphify.report import generate
from pathlib import Path

extraction = json.loads(Path('graphify-out/.graphify_extract.json').read_text())
detection  = json.loads(Path('graphify-out/.graphify_detect.json').read_text())
analysis   = json.loads(Path('graphify-out/.graphify_analysis.json').read_text())

G = build_from_json(extraction, directed=True)
communities = {int(k): v for k, v in analysis['communities'].items()}
cohesion = {int(k): v for k, v in analysis['cohesion'].items()}
tokens = {'input': extraction.get('input_tokens', 0), 'output': extraction.get('output_tokens', 0)}

# LABELS
labels = {
    0: "Adaptive Scheduler & Performance Analytics",
    1: "Base Platform Interface",
    2: "AI Studio Browser Automation",
    3: "Dashboard UI Logic (Frontend)",
    4: "Channel Management API",
    5: "Instagram Graph Publisher",
    6: "Content Generation & Enrichment Pipeline",
    7: "Gemini Image Generation (Browser)",
    8: "Database CRUD Operations",
    9: "Image Compositing & Branding",
    10: "Browser Profile & Media Publisher Helpers",
    11: "Carousel Builder Logic",
    12: "Music Selector & Jamendo Client",
    13: "Prompt & Template Management",
    14: "Scheduled Pipeline Jobs",
    15: "Story Formatter (9:16 images)",
    16: "YouTube RSS Monitoring",
    17: "Groq LLM Client",
    18: "Caption & Hashtag Generation",
    19: "Video Creation (Slideshow/Stories)",
    20: "YouTube Channel Management",
    21: "Feedback Loop & Strategy Adjustment",
    22: "Posting Rate Limiter (PKT based)",
    23: "YouTube Transcript Extraction",
    24: "LLM Response Parser",
    25: "APScheduler Job Management",
    26: "Post Planner & Strategy",
    27: "Platform Content Adapter",
    28: "Facebook Graph Publisher",
    29: "Media Uploader (Public URLs)",
    30: "YouTube Metadata Extraction (yt-dlp)",
    31: "Analytics Collector",
    32: "Performance Booster (Crossposting)",
    33: "FastAPI App Factory",
    34: "Priority Manager (Engagement Scoring)",
    35: "Facebook Page Publisher"
}
# Default rest to "Internal/Init"
for i in range(36, 53):
    labels[i] = "Internal/Init"

# Regenerate questions
questions = suggest_questions(G, communities, labels)

report = generate(G, communities, cohesion, labels, analysis['gods'], analysis['surprises'], detection, tokens, 'src', suggested_questions=questions)
Path('graphify-out/GRAPH_REPORT.md').write_text(report, encoding='utf-8')
Path('graphify-out/.graphify_labels.json').write_text(json.dumps({str(k): v for k, v in labels.items()}))
print('Report updated with community labels')
