#!/usr/bin/env pwsh

# User Display System Test Runner
# PowerShell script for Windows

param(
    [switch]$Verbose,
    [switch]$Coverage,
    [switch]$Performance
)

Write-Host "User Display System - Test Runner" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

# Check if virtual environment exists
$venvPath = "venv"
if (-not (Test-Path $venvPath)) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv $venvPath
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "$venvPath\Scripts\Activate.ps1"

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Run tests
Write-Host "Running tests..." -ForegroundColor Green

$testArgs = @("tests", "-v")

if ($Coverage) {
    $testArgs += @("--cov=user_display", "--cov=user_display_optimized", "--cov-report=html", "--cov-report=term")
}

if ($Performance) {
    $testArgs += @("--benchmark-only")
}

if ($Verbose) {
    $testArgs += @("-s", "--tb=long")
}

try {
    & python -m pytest $testArgs
    $exitCode = $LASTEXITCODE

    if ($exitCode -eq 0) {
        Write-Host "`nAll tests passed! ✅" -ForegroundColor Green

        # Show performance metrics
        Write-Host "`nPerformance Summary:" -ForegroundColor Cyan
        Write-Host "====================" -ForegroundColor Cyan

        # Run a quick performance test
        Write-Host "Running performance validation..." -ForegroundColor Yellow
        python performance_test.py

    } else {
        Write-Host "`nSome tests failed! ❌" -ForegroundColor Red
        exit $exitCode
    }

} catch {
    Write-Host "Error running tests: $_" -ForegroundColor Red
    exit 1
} finally {
    # Deactivate virtual environment
    & deactivate
}

Write-Host "`nTest run completed." -ForegroundColor Green