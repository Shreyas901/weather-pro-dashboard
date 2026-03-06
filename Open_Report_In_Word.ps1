# Weather Pro Report - Open in Microsoft Word
# This script opens the generated HTML report in Microsoft Word for professional formatting

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "    Weather Pro - Opening Report in Word" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

$reportPath = "E:\WeatherReportAPP\Weather_Pro_Report.html"

# Check if the report file exists
if (Test-Path $reportPath) {
    Write-Host "✅ Report file found: $reportPath" -ForegroundColor Green
    Write-Host "📄 Opening in Microsoft Word..." -ForegroundColor Yellow
    
    try {
        # Try to open with Microsoft Word
        Start-Process "winword.exe" -ArgumentList $reportPath -ErrorAction Stop
        Write-Host "✅ Successfully opened in Microsoft Word!" -ForegroundColor Green
        Write-Host ""
        Write-Host "💡 In Word, you can:" -ForegroundColor Cyan
        Write-Host "   • Save as .docx format" -ForegroundColor White
        Write-Host "   • Apply additional formatting" -ForegroundColor White  
        Write-Host "   • Add headers and footers" -ForegroundColor White
        Write-Host "   • Insert page numbers" -ForegroundColor White
        Write-Host "   • Export as PDF" -ForegroundColor White
        
    } catch {
        Write-Host "⚠️  Microsoft Word not found. Trying default browser..." -ForegroundColor Yellow
        Start-Process $reportPath
        Write-Host "✅ Opened in default browser. You can copy content to Word manually." -ForegroundColor Green
    }
    
} else {
    Write-Host "❌ Report file not found: $reportPath" -ForegroundColor Red
    Write-Host "Please ensure the report has been generated first." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Report Details:" -ForegroundColor Cyan
Write-Host "• File: Weather_Pro_Report.html" -ForegroundColor White
Write-Host "• Location: E:\WeatherReportAPP\" -ForegroundColor White
Write-Host "• Format: HTML (Word Compatible)" -ForegroundColor White
Write-Host "• Content: Complete Weather Pro Documentation" -ForegroundColor White
Write-Host "================================================" -ForegroundColor Cyan

Read-Host "Press Enter to close..."