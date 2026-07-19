@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if errorlevel 1 (
    echo Python launcher not found on PATH.
    exit /b 1
)

py -m pip show PyInstaller >nul 2>nul
if errorlevel 1 (
    echo PyInstaller is not installed. Installing it now...
    py -m pip install PyInstaller
    if errorlevel 1 (
        echo Failed to install PyInstaller.
        exit /b 1
    )
)

py -m PyInstaller --onefile --console --name GW2_AutoClicker auto_clicker.py
if errorlevel 1 (
    echo Build failed.
    exit /b 1
)

echo.
echo Build complete.
echo EXE output: dist\GW2_AutoClicker.exe
exit /b 0
