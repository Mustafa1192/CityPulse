from pathlib import Path
from streamlit.testing.v1 import AppTest
ROOT=Path(__file__).resolve().parent
at=AppTest.from_file(str(ROOT/'app.py'),default_timeout=60).run()
assert not at.exception,[e.message for e in at.exception]
assert at.title[0].value=='CityPulse'
views=['Overview','Heat Intelligence','Rain Intelligence','Combined Insights','Evaluation','Data & Method']
for v in views:
    at.sidebar.radio[0].set_value(v).run()
    assert not at.exception,(v,[e.message for e in at.exception])
    print('PASS view:',v)
at.sidebar.radio[0].set_value('Overview').run()
at.sidebar.slider[0].set_value((2024,2025)).run()
assert not at.exception
assert at.metric[0].value=='731',at.metric[0].value
at.sidebar.radio[0].set_value('Combined Insights').run()
assert not at.exception
print('PASS filter 2024–2025: 731 days; Combined view reload.')
print('PASS all app checks.')
