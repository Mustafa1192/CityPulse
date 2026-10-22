"""CityPulse reproducible offline analysis. Run: python pipeline.py"""
from pathlib import Path
import json, hashlib
import numpy as np
import pandas as pd
ROOT = Path(__file__).resolve().parent
MAP = {'T2M_MAX':'tmax_c','T2M_MIN':'tmin_c','T2M':'tmean_c','PRECTOTCORR':'rain_mm'}

def clean(raw):
    frame = pd.DataFrame(raw['properties']['parameter']).rename(columns=MAP)
    frame.index = pd.to_datetime(frame.index, format='%Y%m%d')
    frame.index.name = 'date'
    frame = frame.sort_index().replace(raw['header']['fill_value'], np.nan)
    if frame.index.duplicated().any():
        raise ValueError('Duplicate dates; do not silently aggregate')
    frame = frame.reindex(pd.date_range('2015-01-01','2025-12-31',name='date'))
    # Reject impossible values rather than treating physical extremes as outliers.
    bad = (frame.rain_mm < 0) | (frame.tmin_c > frame.tmax_c) | (frame.tmean_c < frame.tmin_c) | (frame.tmean_c > frame.tmax_c)
    if bad.any():
        raise ValueError('Physical consistency check failed')
    return frame

def thresholds(df):
    train = df.loc['2015':'2021']
    return {'heat_p90_c':float(train.tmax_c.quantile(.90)),
            'heat_p95_c':float(train.tmax_c.quantile(.95)),
            'rain_wet_p95_mm':float(train.loc[train.rain_mm >= 1,'rain_mm'].quantile(.95)),
            'rain_wet_p99_mm':float(train.loc[train.rain_mm >= 1,'rain_mm'].quantile(.99)),
            'fit_start':'2015-01-01','fit_end':'2021-12-31',
            'wet_day_definition':'rain_mm >= 1.0; analytical convention, not an official warning'}

def signals(df, t):
    df = df.copy()
    df['heat_signal'] = np.select([df.tmax_c.isna(),df.tmax_c >= t['heat_p95_c'],df.tmax_c >= t['heat_p90_c']],['Unknown','High','Elevated'],default='Typical')
    df['rain_signal'] = np.select([df.rain_mm.isna(),df.rain_mm >= t['rain_wet_p99_mm'],df.rain_mm >= t['rain_wet_p95_mm']],['Unknown','High','Elevated'],default='Typical')
    df['rain_3day_mm'] = df.rain_mm.rolling(3,min_periods=3).sum()
    df['year'] = df.index.year
    df['month'] = df.index.month
    df['heat_event'] = (df.tmax_c >= t['heat_p95_c']).where(df.tmax_c.notna())
    df['rain_event'] = (df.rain_mm >= t['rain_wet_p95_mm']).where(df.rain_mm.notna())
    return df

def binary_metrics(y, pred):
    y, pred = np.asarray(y,dtype=bool),np.asarray(pred,dtype=bool)
    tp=int((y & pred).sum()); fp=int((~y & pred).sum()); fn=int((y & ~pred).sum()); tn=int((~y & ~pred).sum())
    return {'tp':tp,'fp':fp,'fn':fn,'tn':tn,'precision':tp/(tp+fp) if tp+fp else 0.,'recall':tp/(tp+fn) if tp+fn else 0.,'f1':2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0.,'accuracy':(tp+tn)/len(y)}

def evaluate(df):
    """One-day-ahead retrospective experiment; never features from target day."""
    train = df.loc['2015':'2021']
    rows=[]
    for variable,event in [('tmax_c','heat_event'),('rain_mm','rain_event')]:
        clim=train.groupby(train.index.month)[variable].mean()
        event_clim=train.groupby(train.index.month)[event].mean()
        # Predict target date from yesterday's available value / training month means.
        persist=df[variable].shift(1)
        seasonal=pd.Series(df.index.month.map(clim),index=df.index,dtype=float)
        prob_persist=df[event].astype(float).shift(1)
        prob_clim=pd.Series(df.index.month.map(event_clim),index=df.index,dtype=float)
        for split,a,b in [('validation','2022','2023'),('test','2024','2025')]:
            for method,pred,prob in [('persistence',persist,prob_persist),('seasonal_train_mean',seasonal,prob_clim)]:
                subset=df.loc[a:b]
                ok=subset[variable].notna() & pred.reindex(subset.index).notna() & subset[event].notna() & prob.reindex(subset.index).notna()
                sub=subset.loc[ok]; pv=pred.loc[sub.index]; pp=prob.loc[sub.index]
                row={'split':split,'variable':variable,'method':method,'n':len(sub),'event_count':int(sub[event].sum()),'event_rate':float(sub[event].mean()),'mae':float((sub[variable]-pv).abs().mean()),'rmse':float(np.sqrt(((sub[variable]-pv)**2).mean())), 'brier':float(((sub[event].astype(float)-pp)**2).mean())}
                row.update(binary_metrics(sub[event],pp >= .5)); rows.append(row)
    return pd.DataFrame(rows)

def summarize(df):
    annual=df.groupby('year').agg(mean_tmax_c=('tmax_c','mean'),rain_total_mm=('rain_mm','sum'),heat_high_days=('heat_event','sum'),rain_elevated_days=('rain_event','sum'),valid_heat_days=('tmax_c','count'),valid_rain_days=('rain_mm','count'))
    monthly=df.groupby('month').agg(mean_tmax_c=('tmax_c','mean'),mean_tmin_c=('tmin_c','mean'),mean_daily_rain_mm=('rain_mm','mean'))
    monsoon=float(df.loc[df.month.isin([6,7,8,9]),'rain_mm'].sum()/df.rain_mm.sum()*100)
    hottest=int(monthly.mean_tmax_c.idxmax());wettest=int(annual.rain_total_mm.idxmax())
    findings=[{'title':'Seasonal heat peak','text':f'Month {hottest} has the highest 2015–2025 mean daily maximum temperature: {monthly.loc[hottest,"mean_tmax_c"]:.2f} °C. This describes the selected grid cell, not personal heat exposure.'},
              {'title':'Rainfall seasonality','text':f'June–September contributes {monsoon:.1f}% of total precipitation in the 2015–2025 grid-cell series. Drainage maintenance planning can use this seasonal concentration, not individual flood predictions.'},
              {'title':'Wettest study year','text':f'{wettest} has the largest annual precipitation total in this dataset: {annual.loc[wettest,"rain_total_mm"]:.1f} mm. This is not evidence of flood occurrence.'}]
    return annual,monthly,findings

def main():
    rawpath=ROOT/'data/raw/nasa_power_mumbai_2015_2025.json'
    raw=json.loads(rawpath.read_text(encoding='utf-8'))
    df=clean(raw); t=thresholds(df); df=signals(df,t)
    out=ROOT/'outputs';out.mkdir(exist_ok=True)
    df.to_csv(ROOT/'data/clean/mumbai_daily.csv',float_format='%.6f')
    annual,monthly,findings=summarize(df)
    annual.to_csv(out/'annual_summary.csv');monthly.to_csv(out/'monthly_climatology.csv')
    evaluate(df).to_csv(out/'evaluation.csv',index=False)
    (out/'thresholds.json').write_text(json.dumps(t,indent=2),encoding='utf-8')
    (out/'findings.json').write_text(json.dumps(findings,indent=2),encoding='utf-8')
    qc={'expected_days':4018,'actual_days':len(df),'missing_by_variable':df[list(MAP.values())].isna().sum().to_dict(),'duplicate_days':int(df.index.duplicated().sum()),'imputation':'None','outlier_handling':'Retain plausible extremes; fail on physical inconsistencies','raw_sha256':hashlib.sha256(rawpath.read_bytes()).hexdigest(),'start':str(df.index.min().date()),'end':str(df.index.max().date())}
    (out/'quality.json').write_text(json.dumps(qc,indent=2),encoding='utf-8')
    print(json.dumps({'quality':qc,'thresholds':t,'findings':findings},indent=2))

if __name__=='__main__':main()
