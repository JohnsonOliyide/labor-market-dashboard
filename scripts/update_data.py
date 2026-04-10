import time
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

URLS = {
    "KCFed_ModelBased_Rstar_Ustar.csv": "https://kcresearch-share.kansascityfed.org/kc-mbnr/KCFed_ModelBased_Rstar_Ustar.csv",
    "UNRATE.csv": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=UNRATE",
    "NROU.csv": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=NROU",
}

def download(url, filename):
    for i in range(3):
        try:
            print(f"Downloading {filename} (attempt {i+1})...")
            r = requests.get(url, headers=HEADERS, timeout=120)
            r.raise_for_status()
            
            with open(filename, "wb") as f:
                f.write(r.content)

            print(f"{filename} updated.")
            return
        
        except Exception as e:
            print(f"Attempt {i+1} failed: {e}")
            time.sleep(5)

    print(f"Skipping {filename} after 3 failed attempts.")

print("Starting update...")

for file, url in URLS.items():
    download(url, file)

print("Done.")
