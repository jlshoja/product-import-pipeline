# PowerShell wrapper to run the automatic pipeline with safe defaults
param(
    [int]$TimeoutSeconds = 3600,
    [int]$SubprocessRetries = 1,
    [switch]$NoResume
)

Write-Host "Running pipeline (PowerShell wrapper)"

if (-not $NoResume) {
    $env:AUTO_RESUME = '1'
    Write-Host "AUTO_RESUME=1 (will resume previous incomplete runs)"
} else {
    Remove-Item Env:\AUTO_RESUME -ErrorAction SilentlyContinue
    Write-Host "AUTO_RESUME disabled (will prompt if previous run incomplete)"
}

$env:PROCESS_TIMEOUT = "$TimeoutSeconds"
$env:PROCESS_SUBPROCESS_RETRY = "$SubprocessRetries"

Write-Host "PROCESS_TIMEOUT=$env:PROCESS_TIMEOUT"
Write-Host "PROCESS_SUBPROCESS_RETRY=$env:PROCESS_SUBPROCESS_RETRY"

python product_extraction/main.py auto
