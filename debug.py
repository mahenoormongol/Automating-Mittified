import asyncio
from playwright.async_api import async_playwright
from pathlib import Path

_TWITTER_PROFILE_DIR = Path("data") / "browser_sessions" / "twitter" / "chrome-profile"

async def test():
    async with async_playwright() as pw:
        ctx = await pw.chromium.launch_persistent_context(
            user_data_dir=str(_TWITTER_PROFILE_DIR),
            headless=True,
            channel="chrome",
            args=["--test-type"],
        )
        page = await ctx.new_page()
        await page.goto("https://x.com/search?q=pakistan%20news&src=typed_query&f=media", wait_until="domcontentloaded")
        await asyncio.sleep(5)
        
        # Check raw images and alt text
        img_data = await page.evaluate('''() => {
            const results = [];
            document.querySelectorAll('img[src*="pbs.twimg.com/media"]').forEach(img => {
                results.push({src: img.src, alt: img.alt});
            });
            return results;
        }''')
        print(f"Raw images found: {len(img_data)}")
        for i, data in enumerate(img_data[:3]):
            print(f"Image {i}:")
            print(f"  src: {data['src']}")
            print(f"  alt: {data['alt']}")
        
        await ctx.close()

if __name__ == "__main__":
    asyncio.run(test())
