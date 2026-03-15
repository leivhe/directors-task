@echo off
chcp 65001 >nul
cd /d "%~dp0"

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
    start "" "C:\Program Files\Microsoft\Edge\Application\msedge.exe" http://localhost:8080
) else (
    start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" http://localhost:8080
)
echo.
echo Trykk Enter naar eksperimentet er ferdig for aa stoppe serveren...
pause >nul
echo Avslutter server...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr "0.0.0.0:8080"') do taskkill /f /pid %%a >nul 2>&1
