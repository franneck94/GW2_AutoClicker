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
exit /b 0
