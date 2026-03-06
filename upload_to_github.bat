@echo off
echo ================================================
echo    WeatherReportAPP GitHub Upload Script
echo ================================================
echo.

REM Check if Git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Git is not installed or not in PATH.
    echo Please install Git from: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo Git is available. Starting upload process...
echo.

REM Initialize git repository
echo [1/6] Initializing Git repository...
git init

REM Add remote repository
echo [2/6] Adding remote repository...
git remote add origin https://github.com/Shreyas901/Shreyas.git

REM Check if remote already exists
git remote -v | findstr origin >nul
if %errorlevel% neq 0 (
    git remote add origin https://github.com/Shreyas901/Shreyas.git
) else (
    echo Remote origin already exists, updating URL...
    git remote set-url origin https://github.com/Shreyas901/Shreyas.git
)

REM Add all files to staging
echo [3/6] Adding files to staging area...
git add .

REM Check if there are files to commit
git diff-index --quiet --cached HEAD >nul 2>&1
if %errorlevel% neq 0 (
    echo [4/6] Creating commit...
    git commit -m "Add WeatherReportAPP - Advanced Weather Dashboard with MCP integration"
) else (
    echo No changes to commit.
)

REM Set main branch
echo [5/6] Setting main branch...
git branch -M main

REM Push to GitHub
echo [6/6] Pushing to GitHub...
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ================================================
    echo     SUCCESS! WeatherReportAPP uploaded to GitHub
    echo ================================================
    echo.
    echo Your project is now available at:
    echo https://github.com/Shreyas901/Shreyas
    echo.
) else (
    echo.
    echo ================================================
    echo     ERROR: Failed to push to GitHub
    echo ================================================
    echo.
    echo Common solutions:
    echo 1. Make sure you're authenticated with GitHub
    echo 2. Check if the repository exists and you have access
    echo 3. Try using a Personal Access Token for authentication
    echo.
)

echo.
pause