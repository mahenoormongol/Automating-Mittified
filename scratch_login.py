import asyncio
from playwright.async_api import async_playwright
from pathlib import Path

_TWITTER_PROFILE_DIR = Path("data") / "browser_sessions" / "twitter" / "chrome-profile"

async def auto_login():
    async with async_playwright() as pw:
        ctx = await pw.chromium.launch_persistent_context(
            user_data_dir=str(_TWITTER_PROFILE_DIR),
            headless=True,
            channel="chrome",
            args=[
                "--disable-blink-features=AutomationControlled",
                "--test-type",
            ],
            viewport={"width": 1280, "height": 900},
        )
        page = await ctx.new_page()
        print("Navigating to Twitter login...")
        await page.goto("https://x.com/login", wait_until="domcontentloaded")
        
        try:
            print("Entering username...")
            await page.wait_for_selector("input[autocomplete='username']", timeout=10000)
            await page.fill("input[autocomplete='username']", "Noor1872101Noor")
            await page.keyboard.press("Enter")
            
            print("Entering password...")
            await page.wait_for_selector("input[name='password']", timeout=10000)
            await page.fill("input[name='password']", "RU.(4Qu&WF9#(SN")
            await page.keyboard.press("Enter")
            
            print("Waiting for login to complete...")
            # Wait a bit for the page to load after login
            await page.wait_for_url("https://x.com/home", timeout=15000)
            print("Login successful! Session saved.")
        except Exception as e:
            print(f"Login encountered an issue (might need manual verification or captcha): {e}")
            await page.screenshot(path="login_error.png")
            print("Saved screenshot to login_error.png")
            
        await ctx.close()

if __name__ == "__main__":
    asyncio.run(auto_login())
