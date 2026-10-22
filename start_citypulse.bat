@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  python -m venv .venv
  if errorlevel 1 (
    echo Python 3.11+ is required. Install Python and see README.md.
    pause
    exit /b 1
  )
)
".venv\Scripts\python.exe" -c "import streamlit, pandas, plotly" >nul 2>&1
if errorlevel 1 (
  echo Installing project dependencies. Internet is required only for this step.
  ".venv\Scripts\python.exe" -m pip install -r requirements.txt
  if errorlevel 1 (
    echo Dependency installation failed. See README.md.
    pause
    exit /b 1
  )
)
echo Starting CityPulse locally at http://localhost:8501
".venv\Scripts\python.exe" -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
pause
