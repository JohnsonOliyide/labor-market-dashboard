import time
import requests

HEADERS = {"User-Agent": "Mozilla/5.0"}

URLS = {
    "KCFed_ModelBased_Rstar_Ustar.csv": "https://kcresearch-share.kansascityfed.org/kc-mbnr/KCFed_ModelBased_Rstar_Ustar.csv",
    "UNRATE.csv": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=UNRATE",
    "NROU.csv": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=NROU",
}

def download_with_retries(url: str, max_tries: int = 3, timeout: int = 60) -> bytes:
    last_error = None
    for attempt in range(1, max_tries + 1):
        try:
            response = requests.get(url, headers=HEADERS, timeout=timeout)
            response.raise_for_status()
            return response.content
        except Exception as e:
            last_error = e
            print(f"Attempt {attempt} failed for {url}: {e}")
            if attempt < max_tries:
                time.sleep(5)
    raise last_error

print("Starting full data refresh...")

for filename, url in URLS.items():
    print(f"Downloading {filename}...")
    content = download_with_retries(url)
    with open(filename, "wb") as f:
        f.write(content)
    print(f"{filename} updated.")

print("All data updated successfully.")
