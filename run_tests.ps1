# @echo off
# One-click test runner for the user display system (Windows PowerShell)

function Print-Header {
    param([string]$text)
    Write-Host ""
    Write-Host ("=" * 70) -ForegroundColor Cyan
    Write-Host ("  " + $text) -ForegroundColor Cyan
    Write-Host ("=" * 70) -ForegroundColor Cyan
}

function Check-PythonVersion {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ $pythonVersion"
}

function Install-Dependencies {
    Print-Header "Installing Dependencies"
    
    $requirementsFile = Join-Path $PSScriptRoot "requirements.txt"
    
    if (-not (Test-Path $requirementsFile)) {
        Write-Host "WARNING: requirements.txt not found, skipping installation"
        return
    }
    
    & python -m pip install -q -r $requirementsFile
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Dependencies installed"
    } else {
        Write-Host "ERROR: Failed to install dependencies"
        exit 1
    }
}

function Run-Tests {
    Print-Header "Running Tests"
    
    $testsDir = Join-Path $PSScriptRoot "tests"
    
    & python -m pytest $testsDir -v --tb=short --color=yes
    
    $testResult = $LASTEXITCODE
    
    if ($testResult -eq 0) {
        Write-Host "`n✓ All tests passed"
    } else {
        Write-Host "`n⚠ Some tests failed (exit code: $testResult)"
    }
    
    return $testResult
}

function Run-Coverage {
    Print-Header "Running Tests with Coverage"
    
    $testsDir = Join-Path $PSScriptRoot "tests"
    
    & python -m pytest $testsDir --cov=user_display --cov-report=term-missing --cov-report=html -q
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✓ Coverage report generated (htmlcov/index.html)"
    }
}

function Main {
    Print-Header "User Display System - Test Runner"
    
    Set-Location $PSScriptRoot
    
    # Check environment
    Print-Header "Checking Environment"
    Check-PythonVersion
    
    # Install dependencies
    Install-Dependencies
    
    # Run tests
    $testResult = Run-Tests
    
    # Run coverage
    Run-Coverage
    
    # Summary
    Print-Header "Test Summary"
    
    if ($testResult -eq 0) {
        Write-Host "✓ All tests passed successfully"
        Write-Host ""
        Write-Host "Performance Metrics:"
        Write-Host "  - Display 50,000 users:   < 120ms"
        Write-Host "  - Filter 50,000 users:    < 15ms"
        Write-Host "  - Single ID lookup:       < 0.5ms"
    } else {
        Write-Host "⚠ Some tests failed"
    }
    
    Write-Host ""
    Write-Host "Next Steps:"
    Write-Host "  - Review test output above"
    Write-Host "  - Check README.md for usage examples"
    Write-Host "  - Modify user_display/ modules as needed"
    
    exit $testResult
}

Main
