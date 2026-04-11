# Labor Market Tightness Dashboard

This project presents an interactive dashboard that measures labor market tightness in the United States using the unemployment gap approach.

The dashboard combines publicly available data with model-based estimates to provide a real-time view of labor market conditions.

---

## Overview

The dashboard focuses on the unemployment gap, defined as:

Unemployment rate − Natural rate of unemployment (u*)

- If the gap is negative → labor market is tight  
- If the gap is positive → labor market is slack  
- If the gap is near zero → labor market is roughly balanced  

---

## Features

The dashboard presents three complementary approaches:

Option 1: Credible Set View  
Uses the Kansas City Fed model-based u* and its 68% credible set:
- Entire band below zero → tight  
- Entire band above zero → slack  
- Band contains zero → roughly balanced  

Option 2: Standardized Gap View (Sample Standard Deviation)  
Standardizes the unemployment gap using the sample standard deviation of the gap:
- Values below −1 → tight  
- Values above +1 → slack  
- Values between −1 and +1 → roughly balanced  

Option 3: Standardized Gap View (Standard Error)  
Standardizes the unemployment gap using the estimated standard error of the gap:
- Provides a robustness check  
- Interpreted similarly using ±1 thresholds  

---

## Data Sources

Kansas City Fed model-based natural rate (u*)  
https://kcresearch-share.kansascityfed.org/kc-mbnr/

Unemployment rate (UNRATE)  
https://fred.stlouisfed.org/series/UNRATE  

CBO Noncyclical Rate of Unemployment (NROU)  
https://fred.stlouisfed.org/series/NROU  

---

## Automation

This project includes a fully automated data pipeline using GitHub Actions.

How it works:
- Data is automatically downloaded from source providers  
- Full series are refreshed (including revisions)  
- CSV files are updated in the repository  
- The dashboard reflects updates automatically  

Schedule:
- Runs daily (or on-demand)  
- Only commits changes when data updates occur  

---

## Notes on Data

- The CBO series is quarterly and is repeated across months for comparison  
- All data are publicly available  
- Historical revisions are incorporated automatically  

---

## Disclaimer

The views expressed here are solely my own and do not represent those of the Federal Reserve Bank of Kansas City or the Federal Reserve System.

The data used in this dashboard are obtained from publicly available sources. I do not claim ownership of these data.

---

## Author

Johnson Oliyide  
Research Associate, Federal Reserve Bank of Kansas City  

---
