@echo off
setlocal
cd /d "%~dp0"

set "PYTHON_CMD="
where python >nul 2>nul
if not errorlevel 1 set "PYTHON_CMD=python"

if "%PYTHON_CMD%"=="" (
    where py >nul 2>nul
    if not errorlevel 1 set "PYTHON_CMD=py"
)

if "%PYTHON_CMD%"=="" (
    echo No Python interpreter found on PATH.
    exit /b 1
)

if exist requirements.txt (
    echo Installing project requirements...
    %PYTHON_CMD% -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Failed to install requirements.
        exit /b 1
    )
) else (
    echo requirements.txt not found. Continuing without it.
)

%PYTHON_CMD% -m pip show PyInstaller >nul 2>nul
if errorlevel 1 (
    echo PyInstaller is not installed. Installing it now...
    %PYTHON_CMD% -m pip install PyInstaller
    if errorlevel 1 (
        echo Failed to install PyInstaller.
        exit /b 1
    )
)

%PYTHON_CMD% -m PyInstaller --onefile --console --name GW2_AutoClicker auto_clicker.py
if errorlevel 1 (
    echo Build failed.
    exit /b 1
)

echo.
echo Build complete.
echo EXE output: dist\GW2_AutoClicker.exe

if exist "D:\GW2\addons\GW2TP" (
    copy /y "dist\GW2_AutoClicker.exe" "D:\GW2\addons\GW2TP\"
    if errorlevel 1 (
        echo Failed to copy EXE to D:\GW2\addons\GW2TP.
        exit /b 1
    )
    echo Copied EXE to D:\GW2\addons\GW2TP
) else (
    echo Destination folder does not exist: D:\GW2\addons\GW2TP
)

exit /b 0
