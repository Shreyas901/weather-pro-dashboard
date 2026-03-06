@echo off
echo ================================================
echo     WeatherReportAPP - Quick Deploy to GitHub
echo ================================================
echo.

REM Check if Git is available
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Git is not installed. Please install Git first.
    echo Download from: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo Git found. Proceeding with deployment...
echo.

REM Generate static site for GitHub Pages
echo [1/5] Generating static site...
python generate_static.py
if %errorlevel% neq 0 (
    echo ERROR: Failed to generate static site
    pause
    exit /b 1
)

REM Initialize git if needed
echo [2/5] Initializing git repository...
git init

REM Add remote (will skip if already exists)
echo [3/5] Setting up GitHub remote...
git remote add origin https://github.com/Shreyas901/Shreyas.git 2>nul || (
    echo Remote already exists, updating URL...
    git remote set-url origin https://github.com/Shreyas901/Shreyas.git
)

REM Add all files
echo [4/5] Adding files to git...
git add .

REM Commit changes
echo [5/5] Committing and pushing to GitHub...
git commit -m "Deploy WeatherReportAPP with static build"
git branch -M main
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ================================================
    echo           SUCCESS! Deployed to GitHub
    echo ================================================
    echo.
    echo Your project is now available at:
    echo https://github.com/Shreyas901/Shreyas
    echo.
    echo To enable GitHub Pages:
    echo 1. Go to repository Settings
    echo 2. Scroll to Pages section  
    echo 3. Set Source to "GitHub Actions"
    echo 4. Your site will be live at:
    echo    https://shreyas901.github.io/Shreyas/
    echo.
) else (
    echo.
    echo ERROR: Failed to push to GitHub
    echo Please check your authentication and try again.
)

pause