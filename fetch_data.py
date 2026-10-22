from pathlib import Path
import json,urllib.request,datetime,hashlib
ROOT=Path(__file__).resolve().parent
url='https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M_MAX,T2M_MIN,T2M,PRECTOTCORR&community=AG&longitude=72.8777&latitude=19.0760&start=20150101&end=20251231&format=JSON&time-standard=LST'
p=ROOT/'data/raw/nasa_power_mumbai_2015_2025.json';m=ROOT/'data/source_manifest.json'
if p.exists() or m.exists():raise SystemExit('Refusing overwrite: archive existing raw and manifest deliberately before refreshing.')
p.parent.mkdir(parents=True,exist_ok=True)
with urllib.request.urlopen(url,timeout=120) as r:payload=r.read()
o=json.loads(payload)
assert o['header']['start']=='20150101' and o['header']['end']=='20251231'
manifest={'url':url,'accessed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'coordinates_requested':{'latitude':19.076,'longitude':72.8777},'description':'Single representative grid cell, not city-boundary average or station observations','header':o['header'],'geometry':o['geometry'],'parameters':o['parameters'],'sha256':hashlib.sha256(payload).hexdigest()}
p.write_bytes(payload);m.write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('Downloaded; run python pipeline.py and tests.')
