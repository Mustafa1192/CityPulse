# CityPulse — demo and presentation
Submission target: 23 October 2026, 10:00 IST. Add actual team names; no named contribution is fabricated.

## Eight-slide content outline (not a finished designed slide deck)
1. **CityPulse: explain historical weather before claiming risk.** Mumbai representative point, 2015–2025. Target: municipal planning teams/community volunteers. Historical research prototype, not live warnings.
2. **The gap is usable evidence.** Public climate data are hard to turn into interpretable planning signals. Heat outreach and monsoon maintenance need timing context. Do not claim interviews or user validation.
3. **4,018 days, one documented grid-cell series.** NASA POWER Daily API, 4 source variables, no missing/duplicate dates. Raw download, exact URL and hash retained. Coarse reanalysis ≠ station observations or ward resolution.
4. **April is the selected cell's hottest average Tmax month.** Use outputs/seasonal_heat.png and exact numeric finding in outputs/findings.json. These high grid temperatures are not verified station records.
5. **Rain is strongly seasonal, not a flood map.** June–September share and wettest year from findings.json. Use outputs/annual_rain.png. Recommend preventive planning, not flood occurrence prediction.
6. **Transparent signals before black-box models.** Fit 2015–2021 P90/P95 heat and wet-day P95/P99 rain thresholds. Show train/validation/test split and state these are not IMD categories.
7. **Test honestly, don't sell unvalidated forecasts.** Show held-out MAE/RMSE/Brier from outputs/evaluation.csv; compare within each variable. Persistence uses yesterday, seasonal baseline uses training month means. No flood/health labels, operational availability or station validation. No released forecast.
8. **Demo, limitations, next step.** Heat/Rain/Combined views; reproducible offline package. Next: independent station validation, tide/drainage/incident and exposure data, stakeholder testing. Close with “Predict responsibly. Explain evidence. Act proportionately.”

## Three-minute product walkthrough
0:00–0:20 — “CityPulse turns historical heat and rainfall into transparent planning signals. It is not a real-time disaster warning system.”
0:20–0:50 — Overview: show date/location banner, data-source warning, three full-period findings and monthly charts.
0:50–1:20 — Heat Intelligence: show the training P95 line; explain fixed threshold and outreach suggestions. Say explicitly that heat injury is not modelled.
1:20–1:50 — Rain Intelligence: show daily/trailing three-day rainfall; explain pre-monsoon maintenance and absence of drainage/tide data.
1:50–2:10 — Combined: show separate joint signals, no invented combined probability; filter 2024–2025. Selected final date is historical, not today.
2:10–2:40 — Evaluation: show test rows and source-latency warning. Do not imply the best retrospective metric proves operational forecast skill.
2:40–3:00 — Data & Method: source attribution, quality and clean-data download. Close on reproducibility and next independent validation.

## Backup
Open backup_demo.html directly in a browser if Streamlit/Python fails. Charts and data are embedded; no internet required. PNG charts in outputs are additional backups. Local Streamlit screenshots are in outputs/screenshots if generated in the final validation run.

## Judge Q&A
- Is this IMD data? **No. NASA POWER public gridded meteorological reanalysis.** The brief listed IMD/data.gov.in as candidate sources, not mandatory sources.
- Can you predict street flooding? **No. Rain alone and this spatial resolution do not justify that.**
- Why no ML? **Transparent baselines are evaluated first; adding complexity without evidence would misrepresent capability.**
- Why are temperatures high? **They are coarse-grid source values; no station validation/bias correction. Do not quote them as Mumbai official records.**
- Is this a forecast? **Historical signals plus a retrospective one-day baseline evaluation, not a production forecast. Source latency prevents straightforward operational use.**
- Why only one point? **It avoids false ward-level precision. Suitable independent spatial/impact evidence is future work.**
- Is eleven years enough for climate change claims? **No causal climate-change attribution or 30-year climate normal is claimed.**
- Is there any paid service? **No paid core API or secret key. Once dependencies are installed, packaged data and dashboard run offline.**
- Did AI help? **Yes, disclose AI-assisted implementation/documentation if required; team should review code and be able to explain the method.**

## Three-person handover
Person 1: explain source, units, date conventions, raw/clean pipeline, hash and QC; rehearse data question.
Person 2: explain findings, threshold rules, leakage control, baselines and evaluation limitations.
Person 3: run app, filters, fresh-start test, offline fallback and walkthrough.
Shared: review actual competition rubric, add real names, verify submission file limits and deadline, inspect report and rehearse once. No live upload, account change or hackathon submission has been made by this package.
