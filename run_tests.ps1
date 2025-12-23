# Create venv, install deps, run tests and print basic metrics
$ErrorActionPreference = 'Stop'
$venv = "$PWD\.venv"
if (-not (Test-Path $venv)) {
    python -m venv $venv
}
. "$venv\Scripts\Activate.ps1"
pip install -q -r requirements.txt
Write-Host "Running pytest... (performance tests are opt-in via RUN_PERF=1)"
$env:RUN_PERF = $env:RUN_PERF
pytest -q | Tee-Object -Variable out
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

# show simple perf timings if available
python - <<'PY'
from user_display import Metrics
m = Metrics()
for k in ("filter","lookup_hit","lookup_miss"):
    print(k, m.get(k) if hasattr(m, 'get') else None)
PY
Write-Host "All tests passed."
