# Brief-to-deliverable checklist
| Brief requirement | Delivery / evidence |
|---|---|
| Selected city/time/target user | Mumbai representative grid point, 2015–2025; municipal planning/community volunteers; no ward-level claims |
| Public free core datasets | Preserved NASA POWER meteorology; exact URL, access date, API version and raw hash in data/source_manifest.json; no key/payment |
| Temperature and rainfall | Four daily variables, 4,018 calendar days; data dictionary |
| Cleaning/missing/duplicates/outliers | pipeline.py; quality.json; no missing/duplicates or imputation; plausible extremes retained |
| At least three findings | findings.json, report, Overview and three chart PNGs |
| Transparent method before complexity | Fixed train-only P90/P95 heat and wet-day P95/P99 rain rules; no invented calibrated risk score |
| Forecast only if supported | No released forecast; retrospective baselines evaluated and poor rain-event recall documented |
| Chronological evaluation/baseline | Fit 2015–2021, validation 2022–2023, held-out 2024–2025; persistence and training-month baselines; no test tuning |
| Notebook, charts, evaluation/limitations | Executed analysis.ipynb; outputs; technical report |
| Heat/Rain/Combined dashboard | Six-view Streamlit app; all-view AppTest and year-filter smoke test; browser screenshots |
| Evidence/actions/uncertainty | Report/app explain source bias, absent exposure/drainage/tides/incident validation; bounded planning suggestions |
| Compare periods/locations where data supports | Time-period comparisons only; single grid cell does not justify spatial comparisons |
| Reproducible fresh start | README, pinned requirements/lock, offline packaged data, pipeline and tests |
| Backup demo/screenshots | Self-contained backup_demo.html, PNG charts, local app screenshots |
| Team work split | README and DEMO_AND_PRESENTATION.md, roles not fabricated named contributions |
| Presentation | Eight-slide content outline, 3-minute walkthrough and judge Q&A; not a designed PPTX deck |
| Submission | Local package delivered only; no online deployment or hackathon submission |

## Human handover before upload
Actual hackathon rubric/AI policy and team names were not supplied. Team should confirm these, rehearse the demo and submit by the user-provided deadline: 23 October 2026, 10:00 IST. These are submission checks, not claims that the software needs paid services or extra data to run.
