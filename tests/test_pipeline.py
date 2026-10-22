import sys,json,unittest
from pathlib import Path
import pandas as pd
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from pipeline import ROOT,clean,thresholds,signals,evaluate,binary_metrics
class PipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw=json.loads((ROOT/'data/raw/nasa_power_mumbai_2015_2025.json').read_text());cls.df=clean(cls.raw)
    def test_coverage(self):
        self.assertEqual(len(self.df),4018);self.assertFalse(self.df.isna().any().any());self.assertTrue(self.df.index.is_unique)
    def test_units(self):
        self.assertEqual(self.raw['parameters']['PRECTOTCORR']['units'],'mm/day');self.assertEqual(self.raw['parameters']['T2M_MAX']['units'],'C')
    def test_train_only_thresholds(self):
        changed=self.df.copy();changed.loc['2022':,'tmax_c']=999;changed.loc['2022':,'rain_mm']=999
        self.assertEqual(thresholds(self.df),thresholds(changed))
    def test_no_imputation(self):
        raw=json.loads(json.dumps(self.raw));raw['properties']['parameter']['T2M_MAX']['20150101']=-999
        self.assertTrue(pd.isna(clean(raw).iloc[0].tmax_c))
    def test_signal_boundaries(self):
        t=thresholds(self.df);d=self.df.iloc[:2].copy();d['tmax_c']=[t['heat_p90_c'],t['heat_p95_c']];d['rain_mm']=[t['rain_wet_p95_mm'],t['rain_wet_p99_mm']]
        r=signals(d,t);self.assertEqual(r.heat_signal.tolist(),['Elevated','High']);self.assertEqual(r.rain_signal.tolist(),['Elevated','High']);self.assertTrue(r.rain_3day_mm.isna().all())
    def test_test_sizes_and_metrics(self):
        ev=evaluate(signals(self.df,thresholds(self.df)));self.assertEqual(set(ev.loc[ev.split=='test','n']),{731});self.assertEqual(set(ev.loc[ev.split=='validation','n']),{730})
        self.assertTrue(ev[['precision','recall','f1','brier']].apply(lambda s:s.between(0,1).all()).all())
    def test_metrics_known(self):
        m=binary_metrics([1,1,0,0],[1,0,1,0]);self.assertEqual(m['f1'],.5);self.assertEqual(m['accuracy'],.5)
    def test_persistence_shift(self):
        d=signals(self.df,thresholds(self.df));ev=evaluate(d);target=d.loc['2024':'2025','tmax_c'];p=d.tmax_c.shift(1).loc[target.index]
        got=ev.query("split=='test' and variable=='tmax_c' and method=='persistence'").iloc[0].mae
        self.assertAlmostEqual(got,(target-p).abs().mean())
if __name__=='__main__':unittest.main(verbosity=2)
