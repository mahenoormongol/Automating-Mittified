import urllib.request
import urllib.error

channel_ids = [
    "UC_c-RTowPbIlzMkIa_O7s6Q", # Ducky Bhai
    "UC_niYoJcVwf5IVQZ6pJqgrg", # Rajab’s Family
    "UCz0M2pV4jOUUQ88lOd2q08A", # Maaz Safder World
    "UCbOWx-D1d0-CiP9wc-cH93Q"  # Sistrology
]

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

for cid in channel_ids:
    print(f"Testing Channel: {cid}")
    
    # Standard RSS
    url_std = f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}"
    print(f"  Standard: {url_std}")
    try:
        req = urllib.request.Request(url_std, headers=headers)
        with urllib.request.urlopen(req) as response:
            print(f"    Status: {response.status}")
    except urllib.error.HTTPError as e:
        print(f"    HTTP Error: {e.code} - {e.reason}")
    print("-" * 20)
