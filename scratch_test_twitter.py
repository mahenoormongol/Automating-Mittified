import asyncio
import json
import logging
from src.twitter.scraper import TwitterImageScraper

# Configure logging
logging.basicConfig(level=logging.INFO)

async def test():
    print("Testing TwitterImageScraper with a fresh keyword (4 slides)...")
    scraper = TwitterImageScraper(keyword="Islamabad current breaking news", max_images=4)
    downloaded = await scraper.scrape()
    print(f"\nDone! Downloaded images: {downloaded}")

if __name__ == "__main__":
    asyncio.run(test())
