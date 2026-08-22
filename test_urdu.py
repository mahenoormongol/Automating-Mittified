import asyncio
from playwright.async_api import async_playwright
import os
import sys

# Add src to path so we can import the generator
sys.path.insert(0, os.path.abspath('src'))
from generator.brand_compositor import composite_slide_playwright

async def run_test():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Use an existing image from the directory as a background
        bg_path = os.path.abspath("badpic.PNG")
        if not os.path.exists(bg_path):
            bg_path = os.path.abspath("Capture.PNG")
            
        # A different Urdu example
        headline = "نیا سال نیا آغاز"
        body = "آج ہم نے ایک نئے سفر کا آغاز کیا ہے، امید ہے کہ یہ سال سب کے لیے خوشیاں اور کامیابیاں لے کر آئے۔"
        out_path = os.path.abspath("urdu_test_result_2.png")
        
        print("Generating slide...")
        await composite_slide_playwright(
            page=page,
            background_path=bg_path,
            headline=headline,
            body_text=body,
            output_path=out_path,
            is_rtl=True,
            highlight_words=[]
        )
        
        await browser.close()
        print(f"Generated successfully: {out_path}")

asyncio.run(run_test())
