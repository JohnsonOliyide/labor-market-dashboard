import csv
import json
import os
import time
import requests

HEADERS = {"User-Agent": "Mozilla/5.0"}

KC_URL = "https://kcresearch-share.kansascityfed.org/kc-mbnr/KCFed_ModelBased_Rstar_Ustar.csv"

FRED_SERIES = {
    "UNRATE.csv": "UNRATE",
    "NROU.csv": "NROU",
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

def write_fred_csv_from_json(series_id: str, api_key: str, output_filename: str) -> None:
    url = (
        "https://api.stlouisfed.org/fred/series/observations"
        f"?series_id={series_id}&api_key={api_key}&file_type=json"
    )
    print(f"Downloading {series_id} from FRED API...")
    content = download_with_retries(url)
    payload = json.loads(content)

    observations = payload.get("observations", [])
    if not observations:
        raise ValueError(f"No observations returned for {series_id}")

    with open(output_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["DATE", series_id])
        for obs in observations:
            writer.writerow([obs.get("date"), obs.get("value")])

    print(f"{output_filename} updated from FRED API.")

def main():
    fred_api_key = os.environ.get("FRED_API_KEY")
    if not fred_api_key:
        raise EnvironmentError("FRED_API_KEY is not set.")

    print("Starting full data refresh...")

    print("Downloading KCFed_ModelBased_Rstar_Ustar.csv...")
    kc_content = download_with_retries(KC_URL)
    with open("KCFed_ModelBased_Rstar_Ustar.csv", "wb") as f:
        f.write(kc_content)
    print("KCFed_ModelBased_Rstar_Ustar.csv updated.")

    for filename, series_id in FRED_SERIES.items():
        write_fred_csv_from_json(series_id, fred_api_key, filename)

    print("All data updated successfully.")

if __name__ == "__main__":
    main()
