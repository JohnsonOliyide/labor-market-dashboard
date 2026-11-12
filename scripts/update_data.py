"""Refresh public source data, validating every download before replacing files."""
import csv
import io
import math
import tempfile
import time
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parents[1]
KC_URL = 'https://kcresearch-share.kansascityfed.org/kc-mbnr/KCFed_ModelBased_Rstar_Ustar.csv'
SOURCES = {
    'KCFed_ModelBased_Rstar_Ustar.csv': KC_URL,
    'UNRATE.csv': 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=UNRATE',
    'NROU.csv': 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=NROU',
}

def download(url):
    for attempt in range(3):
        try:
            response = requests.get(url, timeout=90)
            response.raise_for_status()
            return response.text
        except requests.RequestException:
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)

def validate(text, filename):
    rows = list(csv.reader(io.StringIO(text)))
    kc = filename.startswith('KCFed')
    start, column = (2, 4) if kc else (1, 1)
    if len(rows) < 30 or (kc and rows[1][0] != 'Date'):
        raise ValueError(f'Invalid CSV for {filename}')
    valid = []
    for row in rows[start:]:
        if len(row) <= column or not row[column].strip() or row[column] == '.':
            continue
        value = float(row[column])
        if not math.isfinite(value) or not 0 <= value <= 30:
            raise ValueError(f'Invalid value for {filename}')
        time.strptime(row[0], '%Y-%m-%d')
        valid.append(row[0])
    if len(valid) < 24 or len(set(valid)) != len(valid):
        raise ValueError(f'Insufficient or duplicate observations for {filename}')
    return max(valid)

def main():
    with tempfile.TemporaryDirectory(dir=ROOT) as directory:
        staged = []
        for filename, url in SOURCES.items():
            text = download(url)
            latest = validate(text, filename)
            existing = ROOT / filename
            if existing.exists() and latest < validate(existing.read_text(), filename):
                raise ValueError(f'Refusing older data for {filename}')
            path = Path(directory) / filename
            path.write_text(text, encoding='utf-8')
            staged.append((path, existing))
            print(f'Validated {filename}, latest observation {latest}')
        for path, destination in staged:
            path.replace(destination)
    print('All data updated successfully.')

if __name__ == '__main__':
    main()
