import requests
import json
import time
from pathlib import Path

# -------------------------
# Configuration
# -------------------------
BASE_URL = "https://api.openalex.org/authors"
FILTER = "last_known_institutions.country_code:IS"
PER_PAGE = 200
EMAIL = "your_email@example.com"  # strongly recommended by OpenAlex
OUTPUT_DIR = Path("openalex_authors_is")

OUTPUT_DIR.mkdir(exist_ok=True)

# -------------------------
# Session with headers
# -------------------------
session = requests.Session()
session.headers.update({
    "User-Agent": f"OpenAlexDownloader (mailto:{EMAIL})"
})

# -------------------------
# Initial parameters
# -------------------------
params = {
    "filter": FILTER,
    "per-page": PER_PAGE,
    "cursor": "*"
}

page = 0
total_downloaded = 0

# -------------------------
# Download loop
# -------------------------
while True:
    page += 1
    print(f"Downloading page {page}...")

    response = session.get(BASE_URL, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()
    results = data.get("results", [])

    if not results:
        print("No more results.")
        break

    # Save page
    output_file = OUTPUT_DIR / f"authors_page_{page:04d}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    total_downloaded += len(results)
    print(f"  Saved {len(results)} authors (total: {total_downloaded})")

    # Get next cursor
    next_cursor = data.get("meta", {}).get("next_cursor")
    if not next_cursor:
        print("No next cursor found. Done.")
        break

    params["cursor"] = next_cursor

    # Be polite
    time.sleep(0.1)

print(f"\nFinished. Total authors downloaded: {total_downloaded}")
