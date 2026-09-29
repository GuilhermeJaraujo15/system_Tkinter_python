@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    python -m venv .venv
    if errorlevel 1 exit /b 1
)
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 exit /b 1
".venv\Scripts\python.exe" -m unittest discover -s tests -v
if errorlevel 1 exit /b 1
".venv\Scripts\python.exe" -m PyInstaller --noconfirm --workpath build\portatil --distpath dist\portatil TaskManager.spec
if errorlevel 1 exit /b 1
".venv\Scripts\python.exe" package_release.py
if errorlevel 1 exit /b 1
echo Pacote gerado: dist\TaskManager-portatil.zip
