# CityPulse — final technical report
## Executive summary
Mumbai representative point, 2015–2025. Historical decision support for municipal planning teams and community volunteers. This is a hackathon prototype, not an official warning or operational forecast service.

## Data and provenance
NASA POWER Daily API v2.10.1, source identifiers ['MERRA2', 'POWER'], accessed 2026-10-22T15:44:23.878Z. Requested point 19.076 N, 72.8777 E. API request, source metadata and raw SHA-256 are in data/source_manifest.json. Preserved raw JSON is included. Meteorological source values represent a roughly 0.5° x 0.625° grid; they are not station observations or a city-boundary average. LST denotes local solar time, not IST. No synthetic data is used.

There are 4018 expected and actual days, no missing values in four source variables and no duplicate dates. No imputation or smoothing was used for daily signals. Plausible extremes were retained; impossible ordering/negative rain fails the pipeline. NASA fill value -999 is converted to missing. Dates are sorted and reindexed to all calendar days. CSV stores six decimals; raw source precision is preserved in JSON. Three-day precipitation requires three valid consecutive days. Quality details: outputs/quality.json.

## Three evidence-backed findings
### Seasonal heat peak
Month 4 has the highest 2015–2025 mean daily maximum temperature: 39.61 °C. This describes the selected grid cell, not personal heat exposure.

### Rainfall seasonality
June–September contributes 91.3% of total precipitation in the 2015–2025 grid-cell series. Drainage maintenance planning can use this seasonal concentration, not individual flood predictions.

### Wettest study year
2019 has the largest annual precipitation total in this dataset: 3387.3 mm. This is not evidence of flood occurrence.

These findings describe the entire study, while dashboard charts can be filtered. Annual totals are comparable because all study years have complete daily coverage (including leap days). The unusually high coarse-cell temperatures are not independently validated against Mumbai station records; source bias/coastal representation is a material uncertainty.

## Transparent historical method
Training only: 2015–2021. Elevated heat is Tmax >= 39.2700 °C (P90); high heat >= 40.1940 °C (P95). Rain thresholds are computed on training wet days (>=1 mm): elevated >= 73.6595 mm/day (P95), high >= 117.8996 mm/day (P99). Threshold displays round for readability; calculations use full precision. These are analytical exceedance signals, not calibrated disaster probabilities, IMD categories or heatwave declarations. All-month heat thresholds emphasize absolute seasonal heat; they do not measure month-specific anomalies. No composite score or unsupported spatial ranking is invented.

## Chronological evaluation
2015–2021 fit; 2022–2023 validation; 2024–2025 held-out test. No tuning or selection on test outcomes. Both baselines are specified in advance. For each target date, persistence uses the preceding calendar day's value. Seasonal mean uses the target calendar month's training-only average. Continuous errors are MAE and RMSE in °C or mm/day. Do not compare errors across units.

For threshold-event experiments, persistence probability is the prior-day event indicator; seasonal probability is training monthly event frequency. Brier score compares probabilities to same-series exceedance outcomes. Precision/recall/F1 use 0.5 probability cutoff; rare-event baseline accuracy can be misleading, so prevalence, TP/FP/FN/TN, recall and Brier are also reported. Undefined precision/F1 are recorded as 0 when no positives are predicted. These experiments cannot validate floods or heat-related injury. They do not account for operational source-publication latency and do not establish deployable next-day forecasting capability. No forecast feature is released to users.

### Numerical results (validation and held-out test)
     split variable              method   n  event_count  event_rate    mae    rmse  brier  tp  fp  fn  tn  precision  recall     f1  accuracy
validation   tmax_c         persistence 730           38      0.0521 0.8157  1.1335 0.0301  27  11  11 681     0.7105  0.7105 0.7105    0.9699
validation   tmax_c seasonal_train_mean 730           38      0.0521 1.6211  2.1452 0.0378   0   0  38 692     0.0000  0.0000 0.0000    0.9479
      test   tmax_c         persistence 731           59      0.0807 0.8403  1.1381 0.0657  35  24  24 648     0.5932  0.5932 0.5932    0.9343
      test   tmax_c seasonal_train_mean 731           59      0.0807 1.5326  2.0643 0.0552   0   0  59 672     0.0000  0.0000 0.0000    0.9193
validation  rain_mm         persistence 730           13      0.0178 3.8972 10.5963 0.0192   6   7   7 710     0.4615  0.4615 0.4615    0.9808
validation  rain_mm seasonal_train_mean 730           13      0.0178 6.4704 13.9291 0.0162   0   0  13 717     0.0000  0.0000 0.0000    0.9822
      test  rain_mm         persistence 731           13      0.0178 5.2500 13.1910 0.0301   2  11  11 707     0.1538  0.1538 0.1538    0.9699
      test  rain_mm seasonal_train_mean 731           13      0.0178 6.6081 15.0007 0.0170   0   0  13 718     0.0000  0.0000 0.0000    0.9822

Held-out interpretation: Tmax persistence MAE is 0.8403 °C versus 1.5326 °C for the seasonal mean, but its event Brier score (0.06566) is worse than the seasonal probability baseline (0.05515). Rainfall persistence MAE is 5.2500 mm/day versus 6.6081 mm/day for the seasonal mean, but rain-exceedance recall is only 2/13 = 15.4%, with 11 false alarms. Rain Brier is also worse for persistence (0.03010 versus 0.01696). Lower continuous error does not imply reliable event warnings. No operational forecast is released.

No statistical confidence intervals or station-level bias correction were estimated. Results are empirical errors for this dataset, not uncertainty bounds for a new real-world prediction. Forecast complexity was intentionally deferred given the evidence and deadline.

## Practical recommendations
- Before hot-season periods: review shaded rest/water access and outdoor-worker outreach. Use current official advisories for actions.
- Before the monsoon: prioritize drain inspection and maintenance scheduling; use local incident/tide/drainage evidence for site-specific action.
- Publish clear time scope, source type and limitations whenever sharing results. Historical seasonal planning is justified; street-level flood alerts are not.

## Limitations and next validation work
Single coarse grid cell, no station validation, no humidity/heat index, no population vulnerability, tides, terrain, drainage, land use or flood incidents. No ward comparison, no causal climate-change attribution from eleven years, no live observations, and no future disaster predictions. A longer record and independent IMD station series should precede operational thresholds. Validate event definitions against observed impacts before calling indicators risk probabilities. NASA documents nontrivial daily precipitation errors; local accuracy is not established here.

## Reproducibility and implementation
Run pipeline.py to reproduce cleaned CSV, summaries, findings, thresholds, quality and evaluation offline. Run unittest discovery and Streamlit AppTest checks. Start app.py with Streamlit. See README.md. No paid API or credentials are used. The final application and tests are local; there is no public deployment or hackathon submission.

## Three-person handover
Person 1: data/raw, data/clean, source_manifest.json, docs/DATA_DICTIONARY.md and quality.json.
Person 2: pipeline.py, analysis.ipynb, outputs charts, thresholds/evaluation/findings and this report.
Person 3: app.py, requirements.txt, tests, README.md, demo script and presentation outline. All three should review definitions and findings. Names and contributions are not invented.

## Attribution and access
The data was obtained from National Aeronautics and Space Administration (NASA) Langley Research Center's Prediction Of Worldwide Energy Resources (POWER) project funded through the NASA Earth Science Division.
The data was obtained from the POWER Project's Daily API v2.10.1 version on 2026-10-22.
NASA acknowledgment and exact source citation are retained. No NASA endorsement is implied. NASA general open-data guidance applies subject to marked restrictions/third-party material; no POWER-specific Creative Commons license is invented. POWER requests notification of publication or redistribution; no email was sent on your behalf.

## References
- NASA POWER Daily API: https://power.larc.nasa.gov/docs/services/api/temporal/daily/
- Meteorology methodology: https://power.larc.nasa.gov/docs/methodology/meteorology/
- Precipitation validation: https://power.larc.nasa.gov/docs/methodology/meteorology/precipitation/
- POWER referencing: https://power.larc.nasa.gov/docs/referencing/
- NASA data-use guidance: https://www.earthdata.nasa.gov/engage/open-data-services-software-policies/data-use-guidance

Exact download URL: https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M_MAX,T2M_MIN,T2M,PRECTOTCORR&community=AG&longitude=72.8777&latitude=19.0760&start=20150101&end=20251231&format=JSON&time-standard=LST
