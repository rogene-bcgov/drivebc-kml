@echo off
echo DriveBC to KML Converter
echo ========================

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo Python found!

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo Failed to install dependencies
    pause
    exit /b 1
)

REM Run the converter
echo Running DriveBC to KML Converter...
python drivebc_to_kml.py

pause
