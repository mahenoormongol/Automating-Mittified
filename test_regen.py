"""Regenerate slides to test brand_compositor fixes."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from src.generator.brand_compositor import composite_slide
from pathlib import Path

CONTENT_DIR = Path(r"E:\Automating Mittified\data\media\content\2026-05-03\New water tube mai basil & Kamil me boht enjoy kiya😍 ghar Kia howa tha😳")
ENHANCED_DIR = CONTENT_DIR / "enhanced"
OUT_DIR = CONTENT_DIR / "slides"

slides = [
    {
        "frame": "enhanced_XG-0qaHv0f4_s01.png",
        "out": "mittified_XG-0qaHv0f4_s01.png",
        "headline": "MAAZ SAFDER GHAR MEIN DRAMA",
        "body": "Basil aur Kamil ki pool party ke baad ghar mein boht drama hua jab sab ko pata chala kya hua tha",
        "highlights": [],
    },
    {
        "frame": "enhanced_XG-0qaHv0f4_s02.png",
        "out": "mittified_XG-0qaHv0f4_s02.png",
        "headline": "WASHROOM MEIN KYA HUA",
        "body": "Meeting se pehle Maaz ki wife ne bete ko washroom mein band kiya taake shake jaldi khatam",
        "highlights": ["washroom"],
    },
    {
        "frame": "enhanced_XG-0qaHv0f4_s03.png",
        "out": "mittified_XG-0qaHv0f4_s03.png",
        "headline": "PERFUME BRAND BIG EXPANSION",
        "body": "Maaz aur unki team ne poore Pakistan mein apna perfume brand expand karne ka plan share kiya",
        "highlights": [],
    },
    {
        "frame": "enhanced_XG-0qaHv0f4_s04.png",
        "out": "mittified_XG-0qaHv0f4_s04.png",
        "headline": "NEW WATER TUBE EXPOSED",
        "body": "Washroom ke andar naya colorful pool inflate kar diya gaya.",
        "highlights": [],
    },
    {
        "frame": "enhanced_XG-0qaHv0f4_s05.png",
        "out": "mittified_XG-0qaHv0f4_s05.png",
        "headline": "BASIL KAMIL KI POOL PARTY",
        "body": "Dono bacchon ne naye pool mein khoob maze kiye magar parents ke ghar kuch ajeeb hua",
        "highlights": [],
    },
]

for s in slides:
    frame_path = str(ENHANCED_DIR / s["frame"])
    out_path = str(OUT_DIR / s["out"])
    if not Path(frame_path).exists():
        print(f"SKIP (no frame): {s['frame']}")
        continue
    print(f"Compositing: {s['out']} ...")
    composite_slide(
        background_path=frame_path,
        headline=s["headline"],
        body_text=s["body"],
        output_path=out_path,
        slide_number=1,
        total_slides=5,
        highlight_words=s["highlights"],
    )
    print(f"  -> saved {s['out']}")

print("\nDone! Check the slides directory.")
