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
    "C:\Program Files\Microsoft\Edge\Application\msedge.exe" --kiosk http://localhost:8080 --edge-kiosk-type=fullscreen --no-first-run
) else (
    "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --kiosk http://localhost:8080 --edge-kiosk-type=fullscreen --no-first-run
)
echo Trykk Ctrl+C for å stoppe serveren.
pause >nul
