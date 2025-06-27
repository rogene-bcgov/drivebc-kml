@echo off
REM DriveBC KML Service Setup Script for Windows
REM This script helps you set up the service on GitHub

echo 🚗 DriveBC KML Service Setup
echo ==============================

REM Check if we're in a git repository
if not exist ".git" (
    echo ❌ This is not a git repository. Please run 'git init' first.
    pause
    exit /b 1
)

echo ✅ Git repository detected

REM Test the service script
echo 🧪 Testing service script...
python drivebc_service.py
if %ERRORLEVEL% neq 0 (
    echo ❌ Service script failed. Please check your internet connection and try again.
    pause
    exit /b 1
)

echo ✅ Service script working correctly

REM Check if KML file was created
if not exist "drivebc_events.kml" (
    echo ❌ KML file not found
    pause
    exit /b 1
)

echo ✅ KML file generated successfully

REM Add files to git
echo 📦 Adding files to git...
git add .
git add drivebc_events.kml

REM Commit files
echo 💾 Committing initial setup...
git commit -m "Initial setup of DriveBC KML service - Added automated service script - Added GitHub Actions workflow - Added web interface - Generated initial KML file"

echo.
echo 🚀 Setup Complete!
echo.
echo Next steps:
echo 1. Push to GitHub: git push origin main
echo 2. Enable GitHub Pages in repository settings
echo 3. Enable GitHub Actions in repository settings
echo 4. Your service will be available at:
echo    https://yourusername.github.io/yourrepo/
echo.
echo The KML file will auto-update every 30 minutes!
pause
