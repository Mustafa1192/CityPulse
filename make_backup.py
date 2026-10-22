from pathlib import Path
import json,io,contextlib,base64
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import get_plotlyjs
ROOT=Path(__file__).resolve().parent
m=pd.read_csv(ROOT/'outputs/monthly_climatology.csv');a=pd.read_csv(ROOT/'outputs/annual_summary.csv');d=pd.read_csv(ROOT/'data/clean/mumbai_daily.csv');e=pd.read_csv(ROOT/'outputs/evaluation.csv');find=json.loads((ROOT/'outputs/findings.json').read_text());t=json.loads((ROOT/'outputs/thresholds.json').read_text())
figs=[px.line(m,x='month',y='mean_tmax_c',title='Monthly mean daily maximum temperature (°C)'),px.bar(a,x='year',y='rain_total_mm',title='Annual precipitation total (mm)'),px.bar(a,x='year',y='heat_high_days',title='Days above training heat P95')]
for fig in figs:fig.update_layout(template='plotly_dark',paper_bgcolor='#102537',plot_bgcolor='#102537',font={'family':'Arial','size':16})
parts='\n'.join(fig.to_html(full_html=False,include_plotlyjs=False) for fig in figs)
findhtml=''.join('<article><h2>'+x['title']+'</h2><p>'+x['text']+'</p></article>' for x in find)
html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>CityPulse — Offline evidence demo</title><style>*{box-sizing:border-box}body{margin:0;background:#071624;color:#e6f0f6;font:18px/1.5 Arial,sans-serif}main{max-width:1150px;margin:auto;padding:45px 30px}h1{font-size:72px;letter-spacing:-3px;margin:8px 0}h2{line-height:1.2}p{max-width:85ch}article{padding:24px;background:#102537;border-left:4px solid #64c8c4;margin:20px 0}.warn{padding:20px;background:#422e17;color:#ffe1b1}.plotly-graph-div{margin:20px 0}table{border-collapse:collapse;font-size:14px;display:block;overflow:auto}td,th{padding:8px;border:1px solid #345269}a{color:#8ee4e0}.eyebrow{color:#8ee4e0;letter-spacing:3px;text-transform:uppercase;font-size:14px}details{padding:20px;background:#102537;margin-top:20px}footer{margin-top:36px;color:#a6bfce}</style><script>'''+get_plotlyjs()+'''</script><main><div class="eyebrow">HackAMatch 1.0 · Offline demo</div><h1>CityPulse</h1><p>Mumbai · Heat & Rain Intelligence · 2015–2025</p><div class="warn">Historical gridded reanalysis, not station observations, real-time weather, an official warning or a flood forecast. One representative point does not resolve Mumbai wards or streets.</div><p>4,018 daily records · four source variables · no missing source values · no paid API or key · charts are interactive and embedded.</p>'''+findhtml+parts+'''<h2>Transparent signals</h2><p>Thresholds fit on 2015–2021 only: heat elevated/high P90/P95; rain elevated/high wet-day P95/P99 (wet ≥1 mm/day). They are study choices, not IMD categories.</p><pre>'''+json.dumps(t,indent=2)+'''</pre><h2>Chronological baseline evaluation</h2><p>Validation 2022–2023; held-out test 2024–2025. Persistence uses yesterday; seasonal averages use training data only. Temperature errors use °C, rain errors mm/day. Brier measures probability error against same-series threshold exceedance, not real-world impacts.</p>'''+e.round(4).to_html(index=False,border=0)+'''<details><summary>Why this is not a live prediction system</summary><p>NASA source publication latency, no independent station/impact validation, and no tide/drainage/exposure inputs. No ward ranking, flood occurrence or health-outcome claim. High gridded temperatures are not verified Mumbai station records. Eleven years is not a 30-year climate normal. Precision/F1 may be zero for rare-event baselines predicting no positives; inspect event counts and confusion metrics.</p></details><h2>Practical next steps</h2><p>Use historical hot-season patterns to plan shade, water and worker outreach. Use monsoon concentration to schedule drain inspection. Confirm decisions against current IMD and municipal advisories and independent local evidence.</p><footer>NASA Langley Research Center POWER project, funded through NASA Earth Science Division. Daily API v2.10.1. Exact download date/URL/hash are packaged in data/source_manifest.json. No NASA endorsement.<br><a href="https://power.larc.nasa.gov/docs/services/api/temporal/daily/">API documentation</a> · <a href="https://power.larc.nasa.gov/docs/methodology/meteorology/">Source methodology</a> · <a href="https://power.larc.nasa.gov/docs/referencing/">Attribution</a><p>For the full six-view application and year filter, run the packaged Streamlit app. This standalone backup contains full-study charts, findings and evaluation; no Python/server is needed.</p></footer></main></html>'''
(ROOT/'backup_demo.html').write_text(html,encoding='utf-8')
# Execute notebook cells, preserve stream/plain text results and chart outputs.
nbpath=ROOT/'analysis.ipynb';nb=json.loads(nbpath.read_text());env={'__name__':'__notebook__'}
import os,ast
os.chdir(ROOT)
for i,cell in enumerate(c for c in nb['cells'] if c['cell_type']=='code'):
    stream=io.StringIO()
    with contextlib.redirect_stdout(stream),contextlib.redirect_stderr(stream):
        tree=ast.parse(''.join(cell['source']));last=None
        if tree.body and isinstance(tree.body[-1],ast.Expr):last=tree.body.pop()
        exec(compile(tree,'<notebook>','exec'),env)
        if last:
            value=eval(compile(ast.Expression(last.value),'<notebook>','eval'),env)
            if value is not None:print(value)
    cell['execution_count']=i+1;cell['outputs']=[]
    if stream.getvalue():cell['outputs'].append({'output_type':'stream','name':'stdout','text':stream.getvalue().splitlines(True)})
    if 'monthly.mean_tmax_c' in ''.join(cell['source']):
        for name in ['seasonal_heat.png','annual_rain.png','annual_heat.png']:
            cell['outputs'].append({'output_type':'display_data','data':{'image/png':base64.b64encode((ROOT/'outputs'/name).read_bytes()).decode(),'text/plain':['Generated analytical chart']},'metadata':{}})
nbpath.write_text(json.dumps(nb,indent=2),encoding='utf-8')
print('Self-contained backup written; all notebook cells executed successfully.')
