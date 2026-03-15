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
if exist "C:\Program Files\Microsoft\Edge\Application\msedge.exe" (
    "C:\Program Files\Microsoft\Edge\Application\msedge.exe" --start-fullscreen http://localhost:8080 --no-first-run
) else (
    "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --start-fullscreen http://localhost:8080  --no-first-run
)
echo Avslutter server...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr "0.0.0.0:8080"') do taskkill /f /pid %%a >nul 2>&1
echo Ferdig.
timeout /t 2 /nobreak >nul
