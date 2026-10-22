# Data dictionary
Source: NASA POWER Daily point API v2.10.1. Source meteorology is gridded reanalysis, not station observations. Full raw metadata, exact URL and access date: ../data/source_manifest.json.

| Clean field | Source | Unit / definition |
|---|---|---|
| date | YYYYMMDD source keys | Calendar day, LST local solar time; not IST |
| tmax_c | T2M_MAX | °C; maximum 2 m temperature derived from hourly source values |
| tmin_c | T2M_MIN | °C; minimum 2 m temperature |
| tmean_c | T2M | °C; daily mean 2 m temperature |
| rain_mm | PRECTOTCORR | Source units mm/day; daily rate numerically interpreted as 1-day depth mm for daily sums |
| heat_signal | training quantiles of tmax_c | Typical <P90; Elevated ≥P90 and <P95; High ≥P95; missing → Unknown |
| rain_signal | training quantiles of wet-day rain | Typical <wet P95; Elevated ≥wet P95 and <wet P99; High ≥wet P99; missing → Unknown |
| rain_3day_mm | rain_mm | Current plus previous two calendar days; requires 3 valid days; first two rows missing |
| year, month | date | Integer calendar components |
| heat_event | tmax_c ≥training P95 | Boolean exceedance in reanalysis; not a health event |
| rain_event | rain_mm ≥training wet P95 | Boolean exceedance in reanalysis; not a flood event |

Quantiles use pandas default linear interpolation and training dates 2015-01-01 to 2021-12-31. Wet day ≥1 mm/day is a project convention. Heat uses all days, not a seasonal anomaly. Thresholds remain unchanged under dashboard filters.

## Transformations
1. Preserve API response; SHA-256 raw bytes in manifest and quality report.
2. Parse source date keys; rename four variables; convert declared fill sentinel -999 to missing.
3. Sort and require unique dates. Reindex to 2015-01-01–2025-12-31 (4,018 calendar days).
4. Reject negative rain or temperature ordering inconsistency. No temperature-value capping, outlier removal or imputation.
5. Fit thresholds only on training subset, compute retrospective labels and rolling sums.
6. Write UTF-8 CSV, six decimals; raw original precision retained.

## Aggregate definitions
Annual mean Tmax: mean daily maxima. Annual rain: sum daily rain depth. Heat count: number of days ≥training P95. Rain event count: days ≥training wet P95 (includes High). Monthly climatology: across-study mean daily values by calendar month. June–September rainfall share: sum over those months / sum over all days. Full-study findings do not change with dashboard filters.

## Evaluation columns
MAE/RMSE: continuous error, °C for Tmax or mm/day for rain. Brier: mean squared threshold-event probability error. Predictions at probability ≥0.5 count positive. TP/FP/FN/TN and event_count document imbalance. Precision/recall/F1 are 0 when their denominators vanish. Accuracy alone is not a skill assessment. Validation/test labels are derived from fixed training thresholds. Candidate methods specified in advance; no hold-out tuning. Each year's totals require full source completeness; this snapshot has full completeness.

## Geographic limitations
Single requested Mumbai point (19.076,72.8777) samples coarse model meteorology (~0.5° × 0.625°), not an administrative area. Returned point coordinates are request metadata, not a documented grid footprint. No neighborhood or ward comparison. No station calibration; especially high gridded temperatures should not be represented as official Mumbai extremes.
