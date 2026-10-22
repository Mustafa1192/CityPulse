from pathlib import Path
import json
import pandas as pd
import plotly.express as px
import streamlit as st
ROOT=Path(__file__).resolve().parent
st.set_page_config(page_title='CityPulse | Mumbai',page_icon=None,layout='wide')
st.markdown('''<style>.stApp{background:#071624;color:#e8eff7}h1,h2,h3{letter-spacing:-.025em}div[data-testid="stMetric"]{background:#112b40;border:1px solid #25455e;border-radius:12px;padding:18px}section[data-testid="stSidebar"]{background:#102537} [data-testid="stMarkdownContainer"] p,[data-testid="stMarkdownContainer"] h2,[data-testid="stMarkdownContainer"] h3,[data-testid="stMetricValue"],[data-testid="stMetricLabel"] p,[data-testid="stCaptionContainer"] p,[data-testid="stSidebar"] label{color:#e8eff7!important} [data-testid="stAlert"] p{color:#ffe1b1!important} header[data-testid="stHeader"]{background:#071624!important} [data-testid="stDataFrame"]{background:#102537}</style>''',unsafe_allow_html=True)
@st.cache_data
def load():
    return pd.read_csv(ROOT/'data/clean/mumbai_daily.csv',parse_dates=['date']),json.loads((ROOT/'outputs/thresholds.json').read_text()),json.loads((ROOT/'outputs/quality.json').read_text())
try:d,t,q=load()
except FileNotFoundError:
    st.error('Packaged data is missing. Run python pipeline.py from the project folder.');st.stop()
st.caption('HACKAMATCH 1.0 / HISTORICAL DECISION-SUPPORT PROTOTYPE')
st.title('CityPulse')
st.markdown('### Mumbai · Heat & Rain Intelligence')
st.warning('Historical gridded reanalysis — not station observations, live weather, a flood forecast or an official warning. One representative cell cannot resolve wards or streets.')
st.sidebar.header('Explore the evidence')
view=st.sidebar.radio('View',['Overview','Heat Intelligence','Rain Intelligence','Combined Insights','Evaluation','Data & Method'])
years=st.sidebar.slider('Study years',2015,2025,(2015,2025))
f=d[d.date.dt.year.between(*years)].copy()
st.sidebar.caption('Requested point: 19.076° N, 72.8777° E. NASA POWER meteorology: approximately 0.5° × 0.625°. LST (solar time), not IST.')
st.sidebar.caption('Signal thresholds stay fixed at 2015–2021 training values when filters change.')
COLORS={'Typical':'#6cbcc3','Elevated':'#f2b85a','High':'#f06b68','Unknown':'#9eabb9'}
def chart(fig):
    fig.update_layout(template='plotly_dark',paper_bgcolor='#071624',plot_bgcolor='#0d2234',font_color='#e8eff7',legend_title_text='')
    st.plotly_chart(fig,use_container_width=True,theme=None)
def findings():
    for item in json.loads((ROOT/'outputs/findings.json').read_text()):
        st.subheader(item['title']);st.write(item['text'])
    st.caption('These findings refer to the full 2015–2025 series, not the sidebar subset. They are descriptive, not causal claims.')
if view=='Overview':
    a,b,c,dcol=st.columns(4)
    a.metric('Days in selection',f'{len(f):,}');b.metric('Mean daily Tmax',f'{f.tmax_c.mean():.1f} °C');c.metric('Precipitation total',f'{f.rain_mm.sum():,.0f} mm');dcol.metric('High heat days',int((f.heat_signal=='High').sum()))
    st.caption(f'Selection: {years[0]}–{years[1]}. Rainfall total spans the entire selected period, not a yearly average.')
    monthly=f.groupby(f.date.dt.to_period('M'))[['tmax_c','rain_mm']].agg({'tmax_c':'mean','rain_mm':'sum'}).reset_index();monthly['date']=monthly['date'].astype(str)
    x,y=st.columns(2)
    with x:chart(px.line(monthly,x='date',y='tmax_c',title='Monthly mean of daily maximum temperature',labels={'tmax_c':'°C','date':'Month'}))
    with y:chart(px.bar(monthly,x='date',y='rain_mm',title='Monthly precipitation total',labels={'rain_mm':'mm','date':'Month'}))
    findings()
elif view=='Heat Intelligence':
    st.subheader('Historical heat signals')
    st.write(f"Elevated: Tmax ≥ {t['heat_p90_c']:.2f} °C; High: Tmax ≥ {t['heat_p95_c']:.2f} °C. Training-period empirical P90/P95 of all days. These are not IMD heatwave definitions.")
    fig=px.line(f,x='date',y='tmax_c',labels={'tmax_c':'Maximum temperature (°C)'})
    fig.add_hline(y=t['heat_p95_c'],line_dash='dash',line_color='#f06b68',annotation_text='Training P95');chart(fig)
    ann=f.groupby(f.date.dt.year).agg(mean_tmax=('tmax_c','mean'),high_days=('heat_event','sum')).reset_index()
    chart(px.bar(ann,x='date',y='high_days',title='High heat signal days by year',labels={'date':'Year','high_days':'Days'}))
    st.info('Planning actions: review shaded rest areas and drinking-water access; coordinate outreach to outdoor workers. For operational decisions, consult current IMD/local advisories. Humidity, indoor conditions and vulnerability are not modelled.')
elif view=='Rain Intelligence':
    st.subheader('Historical rainfall signals')
    st.write(f"Elevated: precipitation ≥ {t['rain_wet_p95_mm']:.2f} mm/day; High: ≥ {t['rain_wet_p99_mm']:.2f} mm/day. Quantiles use only training wet days (≥1 mm). These are study-specific signals, not official rainfall categories.")
    chart(px.bar(f,x='date',y='rain_mm',labels={'rain_mm':'Precipitation (mm/day)'}))
    chart(px.line(f,x='date',y='rain_3day_mm',title='Trailing 3-day precipitation total',labels={'rain_3day_mm':'mm'}))
    st.info('Planning actions: prioritize pre-monsoon drain inspection, review maintenance schedules and prepare communication channels. Flooding additionally depends on tides, drainage, terrain, land cover and verified incident data; these are not included.')
elif view=='Combined Insights':
    st.subheader('Two signals, not one invented risk score')
    latest=f.sort_values('date').iloc[-1]
    st.write(f"Selected final historical date: {latest.date.date()} — heat: {latest.heat_signal}; rainfall: {latest.rain_signal}.")
    st.caption('This date is not today and is not a forecast.')
    cross=pd.crosstab(f.heat_signal,f.rain_signal).reindex(index=['Typical','Elevated','High','Unknown'],columns=['Typical','Elevated','High','Unknown'],fill_value=0)
    chart(px.imshow(cross,text_auto=True,color_continuous_scale='Teal',title='Historical joint signal counts',labels={'x':'Rain signal','y':'Heat signal','color':'Days'}))
    annual=f.groupby(f.date.dt.year)[['heat_event','rain_event']].sum().rename(columns={'heat_event':'High heat','rain_event':'Elevated-or-high rain'}).reset_index()
    chart(px.bar(annual,x='date',y=['High heat','Elevated-or-high rain'],barmode='group',labels={'date':'Year','value':'Days'}))
    st.write('Prioritization is by historical time period only. No neighborhood ranking is justified by this dataset. Keep heat outreach and rainfall-maintenance plans separate; joint counts do not establish compound disaster impacts.')
    st.dataframe(f[['date','tmax_c','rain_mm','heat_signal','rain_signal']].sort_values('date',ascending=False),hide_index=True)
elif view=='Evaluation':
    st.subheader('Honest one-day-ahead baseline experiment')
    st.write('Fit: 2015–2021 · Validation: 2022–2023 · Held-out test: 2024–2025. No tuning or model selection on test data. Persistence uses yesterday’s value; seasonal baseline uses training-only calendar-month means. Event probabilities: yesterday’s event (0/1) versus training-only month event frequency. No future target-day input is used.')
    ev=pd.read_csv(ROOT/'outputs/evaluation.csv');st.dataframe(ev,hide_index=True)
    chart(px.bar(ev[ev['split']=='test'],x='variable',y='mae',color='method',barmode='group',title='Held-out MAE — compare within each variable only'))
    st.caption('Temperature errors use °C; rainfall errors use mm/day. Never compare the numerical errors across different units. Precision/recall/F1 use probability threshold 0.5; zero predicted positives gives zero precision/F1. Brier is mean squared probability error (lower is better).')
    st.warning('Evaluation targets threshold exceedances in the same reanalysis series, NOT actual health impacts or floods. No independent station/incident validation, uncertainty interval, operational forecast or forecast skill claim is provided. Weather-source publication latency also prevents treating this as a deployable next-day forecast service.')
elif view=='Data & Method':
    st.subheader('Provenance, quality & reproducibility')
    st.json(q);st.json(t)
    st.write('No imputation. NASA fill values become missing; duplicates and physical inconsistencies fail the pipeline. Plausible extreme values are retained. Three-day rainfall needs three valid days. Raw data and SHA-256 are packaged. An 11-year sample is not a 30-year climate normal or a climate-change attribution study.')
    st.write('The high Tmax values reflect this coarse reanalysis cell and have not been validated against Mumbai stations. Do not represent them as official city records. Coastal grid averaging and source bias can be substantial.')
    st.write('Data: NASA Langley Research Center POWER, Daily API v2.10.1, MERRA2/POWER; full access time and exact URL in data/source_manifest.json. LST is local solar time, not civil IST.')
    st.markdown('[Daily API documentation](https://power.larc.nasa.gov/docs/services/api/temporal/daily/) · [Meteorology method](https://power.larc.nasa.gov/docs/methodology/meteorology/) · [Attribution](https://power.larc.nasa.gov/docs/referencing/)')
    st.caption('The data was obtained from NASA Langley Research Center’s Prediction Of Worldwide Energy Resources (POWER) project funded through the NASA Earth Science Division. No NASA endorsement is implied.')
    st.download_button('Download cleaned data',data=(ROOT/'data/clean/mumbai_daily.csv').read_bytes(),file_name='mumbai_daily.csv',mime='text/csv')
    st.download_button('Download evaluation',data=(ROOT/'outputs/evaluation.csv').read_bytes(),file_name='evaluation.csv',mime='text/csv')
st.divider();st.caption('CITYPULSE · Predict responsibly. Explain evidence. Act proportionately. · Hackathon research prototype, not an operational safety system.')
