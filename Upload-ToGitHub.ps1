# WeatherReportAPP GitHub Upload Script
# PowerShell version

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "    WeatherReportAPP GitHub Upload Script" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Git is installed
try {
    $gitVersion = git --version
    Write-Host "✓ Git is available: $gitVersion" -ForegroundColor Green
}
catch {
    Write-Host "✗ ERROR: Git is not installed or not in PATH." -ForegroundColor Red
    Write-Host "Please install Git from: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Starting upload process..." -ForegroundColor Yellow
Write-Host ""

try {
    # Initialize git repository
    Write-Host "[1/6] Initializing Git repository..." -ForegroundColor Blue
    git init

    # Add remote repository (handle if it already exists)
    Write-Host "[2/6] Adding remote repository..." -ForegroundColor Blue
    try {
        git remote add origin https://github.com/Shreyas901/Shreyas.git
    }
    catch {
        Write-Host "Remote origin already exists, updating URL..." -ForegroundColor Yellow
        git remote set-url origin https://github.com/Shreyas901/Shreyas.git
    }

    # Add all files to staging
    Write-Host "[3/6] Adding files to staging area..." -ForegroundColor Blue
    git add .

    # Create commit
    Write-Host "[4/6] Creating commit..." -ForegroundColor Blue
    git commit -m "Add WeatherReportAPP - Advanced Weather Dashboard with MCP integration"

    # Set main branch
    Write-Host "[5/6] Setting main branch..." -ForegroundColor Blue
    git branch -M main

    # Push to GitHub
    Write-Host "[6/6] Pushing to GitHub..." -ForegroundColor Blue
    git push -u origin main

    # Success message
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Green
    Write-Host "     SUCCESS! WeatherReportAPP uploaded to GitHub" -ForegroundColor Green
    Write-Host "================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your project is now available at:" -ForegroundColor Cyan
    Write-Host "https://github.com/Shreyas901/Shreyas" -ForegroundColor White
    Write-Host ""
}
catch {
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Red
    Write-Host "     ERROR: Failed to upload to GitHub" -ForegroundColor Red
    Write-Host "================================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Error details: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Common solutions:" -ForegroundColor Yellow
    Write-Host "1. Make sure you're authenticated with GitHub" -ForegroundColor White
    Write-Host "2. Check if the repository exists and you have access" -ForegroundColor White
    Write-Host "3. Try using a Personal Access Token for authentication" -ForegroundColor White
    Write-Host "4. Make sure the repository URL is correct" -ForegroundColor White
    Write-Host ""
}

Write-Host ""
Read-Host "Press Enter to exit"