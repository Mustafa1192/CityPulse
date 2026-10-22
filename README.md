# CityPulse — Mumbai Heat & Rain Intelligence
HackAMatch 1.0 · Mumbai representative point · 2015–2025

## Start here
This package contains a **historical decision-support prototype**, not an operational forecast, official warning, street-level flood map or station-observation product. No paid API, account or secret key is required. Packaged public data lets the app run offline after Python dependencies are installed. No public deployment or hackathon submission has been made.

### Windows (PowerShell)
From this folder, with Python 3.11+ installed:
```
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe pipeline.py
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1
```
Open http://localhost:8501. If this delivered workspace already has `.venv`, skip environment creation/install. The ZIP deliberately excludes the environment.

### macOS / Linux
```
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python pipeline.py
.venv/bin/python -m streamlit run app.py --server.address 127.0.0.1
```
Optional Jupyter: install Jupyter separately, select this environment, open `analysis.ipynb` from this folder. The core app does not require Jupyter.

## Run checks
```
.\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py" -v
.\.venv\Scripts\python.exe verify_app.py
```
`verify_app.py` uses Streamlit AppTest to check all six views and the year filter. Test evidence is in `outputs/verification.txt`. Re-run when code changes. `requirements-lock.txt` records the tested resolved environment; `requirements.txt` pins direct dependencies. To exactly reproduce the test environment, install `requirements-lock.txt` instead.

## Files and handover
- `app.py`: six dashboard views: Overview, Heat, Rain, Combined, Evaluation, Data & Method.
- `pipeline.py`: offline cleaning, fixed thresholds, findings, summaries, chronological evaluation.
- `data/raw/`: unmodified NASA POWER response.
- `data/clean/mumbai_daily.csv`: 4,018 daily rows; derived signals.
- `data/source_manifest.json`: exact API request, access date, returned source metadata, raw hash.
- `analysis.ipynb`: reproducible exploratory analysis notebook; generated and programmatically executed in validation.
- `outputs/`: findings, thresholds, QC, all baseline metrics, three PNG charts and checks.
- `docs/REPORT.md` and `docs/CityPulse_Submission_Report.docx`: final report; Word content/package validation only unless a separate rendered-layout result is supplied.
- `docs/DATA_DICTIONARY.md`: units/definitions and transformation rules.
- `docs/DEMO_AND_PRESENTATION.md`: presentation outline, three-person handover, 3-minute walkthrough and Q&A.
- `backup_demo.html`: offline interactive chart demo and evidence fallback, no Python/server/network required.

## Method in one minute
Fit all empirical thresholds on 2015–2021 only. Heat Elevated/High are all-day Tmax P90/P95. Rain Elevated/High are wet-day P95/P99 (wet >=1 mm/day). These are **analytical choices**, not IMD warning categories. Dashboard year filters do not refit thresholds. Three-day rainfall sums require three valid days.

Evaluate two pre-specified one-day-ahead baselines: yesterday's value and training monthly mean. Validation 2022–2023; untouched held-out test 2024–2025. Evaluate continuous MAE/RMSE, and threshold-event precision/recall/F1/confusion counts/Brier with event probability cutoff 0.5. Target outcomes are exceedances in the same reanalysis, not independently verified impacts. Source publication latency means the experiment is not an operational forecast service. No complex model or future forecast is claimed.

## Data integrity and scope
NASA POWER Daily API v2.10.1, MERRA2/POWER response. Requested point 19.076 N, 72.8777 E; source meteorology is roughly 0.5° x 0.625°, not street/ward resolution or Mumbai boundary average. Date is local solar time (LST), not IST. Four source variables: daily Tmax/Tmin/Tmean (°C), PRECTOTCORR (mm/day). No missing data or duplicates in downloaded series; no imputation. Fill -999 becomes missing. Physical inconsistency raises an error. Plausible extremes are retained, not winsorized. Exact provenance and SHA-256 travel with the data.

The high gridded Tmax values are **not verified Mumbai station records**. Rainfall alone cannot establish flooding; heat exposure also depends on humidity, shelter and vulnerability. No real-time monitoring, ward ranking, disaster probability calibration or causal climate-change attribution is provided. Consult current IMD/municipal advisories before action. Eleven years is not a standard 30-year climate normal.

## Data refresh (optional; internet required)
Run `python fetch_data.py` to fetch the exact same fixed-period request. It refuses to overwrite existing raw/manifest files: archive them deliberately first if you want a new version. Raw files should remain fixed for the judged demo; archive revisions can otherwise change results. After a deliberate refresh, rerun pipeline and tests. Do not repeatedly download identical grid-cell data.

## Attribution and reuse
The data was obtained from National Aeronautics and Space Administration (NASA) Langley Research Center's Prediction Of Worldwide Energy Resources (POWER) project funded through the NASA Earth Science Division. Service: POWER Daily API 2.10.1; exact retrieval time: `data/source_manifest.json`.

- https://power.larc.nasa.gov/docs/referencing/
- https://power.larc.nasa.gov/docs/services/api/temporal/daily/
- https://power.larc.nasa.gov/docs/methodology/meteorology/
- https://power.larc.nasa.gov/docs/methodology/meteorology/precipitation/
- https://www.earthdata.nasa.gov/engage/open-data-services-software-policies/data-use-guidance

NASA's general open-data use guidance permits factual educational/informational reuse with acknowledgment, subject to marked restrictions/third-party content. Do not imply NASA endorsement or claim a specific POWER Creative Commons license not supplied here. POWER requests notification of publication/redistribution; no email has been sent on behalf of the team.

## Submission readiness
Check the actual competition rubric and AI-assistance policy, add real team names/contributions, rehearse locally, and submit before **23 October 2026, 10:00 IST**. No additional hackathon rubric was provided. Do not claim manual authorship if the competition asks about AI assistance. No fabricated user research, performance benchmarks, station validation or judges' approval is included.
