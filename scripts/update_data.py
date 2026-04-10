# Source URLs
urls = {
    "KCFed_ModelBased_Rstar_Ustar.csv": "https://kcresearch-share.kansascityfed.org/kc-mbnr/KCFed_ModelBased_Rstar_Ustar.csv",
    "UNRATE.csv": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=UNRATE",
    "NROU.csv": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=NROU",
}

for filename, url in urls.items():
    print(f"Downloading {filename}...")
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"{filename} updated.")
    else:
        raise Exception(f"Failed to download {filename}")

print("All data updated successfully.")
