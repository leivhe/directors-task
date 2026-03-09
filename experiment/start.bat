@echo off
chcp 65001 >nul

python --version >nul 2>&1
if errorlevel 1 (
    echo Python ble ikke funnet.
    echo Installer Python fra organisasjonens installasjonsside og prøv igjen.
    pause
    exit /b
)

echo Starter eksperimentet...
start "" http://localhost:8080
python -m http.server 8080
