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
start /b python -m http.server 8080
timeout /t 2 /nobreak >nul
start "" http://localhost:8080
echo Trykk Ctrl+C for å stoppe serveren.
pause >nul
