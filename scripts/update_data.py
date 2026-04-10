import requests

headers = {
    "User-Agent": "Mozilla/5.0"
}

urls = {
    "KCFed_ModelBased_Rstar_Ustar.csv": "https://kcresearch-share.kansascityfed.org/kc-mbnr/KCFed_ModelBased_Rstar_Ustar.csv",
    "UNRATE.csv": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=UNRATE",
    "NROU.csv": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=NROU",
}

for filename, url in urls.items():
    print(f"Downloading {filename}...")

    try:
        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"{filename} updated.")
        else:
            print(f"Failed to download {filename} (status {response.status_code})")

    except Exception as e:
        print(f"Error downloading {filename}: {e}")

print("Done.")
