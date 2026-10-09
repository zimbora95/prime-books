# backup-download.ps1 — materialise the Prime Books backup tree on this PC.
#
# Builds   <Destination>\Year NN\<Subject>\<slug>-output.pdf  (+ -input.<ext>)
# from the served pull list. Never deletes, never overwrites a file it cannot
# prove is identical: re-running resumes and skips finished files.
#
#   powershell -ExecutionPolicy Bypass -File backup-download.ps1
#   powershell -ExecutionPolicy Bypass -File backup-download.ps1 -Verify
#   powershell -ExecutionPolicy Bypass -File backup-download.ps1 -Destination "D:\PB Backup"
#
# -Verify re-hashes every local file against the recorded sha256 (slow, ~2 min).

param(
    [string]$Destination = "C:\Users\alexa\Documents\Prime Books",
    [string]$Base        = "",      # blank = use the base recorded in the pull list
    [switch]$Verify
)

$ErrorActionPreference = 'Stop'
$ProgressPreference    = 'Continue'

$listUrl = if ($Base) { "$($Base.TrimEnd('/'))/backup-download.json" }
           else        { "https://methods-museum-quizzes-muscles.trycloudflare.com/backup-download.json" }

Write-Host "fetching pull list: $listUrl" -ForegroundColor Cyan
$list = Invoke-RestMethod -Uri $listUrl -TimeoutSec 60
if (-not $Base) { $Base = $list.base.TrimEnd('/') }
Write-Host "base      : $Base"
Write-Host "generated : $($list.generated)"
Write-Host "destination: $Destination"
Write-Host "files     : $($list.files.Count)"
Write-Host ""

if (-not (Test-Path -LiteralPath $Destination)) {
    New-Item -ItemType Directory -Path $Destination -Force | Out-Null
}

$ok = 0; $skipped = 0; $failed = @()
$done = 0

foreach ($f in $list.files) {
    $done++
    $rel  = $f.dest -replace '/', '\'
    $dest = Join-Path $Destination $rel
    $dir  = Split-Path -Parent $dest
    if (-not (Test-Path -LiteralPath $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }

    $sizeOk = $false
    if (Test-Path -LiteralPath $dest) {
        if ((Get-Item -LiteralPath $dest).Length -eq $f.bytes) { $sizeOk = $true }
    }

    # Trust a same-size local file unless -Verify was asked for.
    if ($sizeOk -and -not $Verify) { $skipped++; continue }

    if ($sizeOk -and $Verify) {
        $h = (Get-FileHash -LiteralPath $dest -Algorithm SHA256).Hash.ToLower()
        if ($h -eq $f.sha256) { $skipped++; continue }
    }

    $url = "$Base/" + (($f.src -split '/') | ForEach-Object { [uri]::EscapeDataString($_) }) -join '/'
    $pct = [int](100 * $done / $list.files.Count)
    Write-Host ("[{0,3}%] {1}" -f $pct, $rel) -ForegroundColor Gray

    # curl.exe ships with Windows 10+ and beats Invoke-WebRequest on big files.
    & curl.exe -L --fail --silent --show-error --retry 3 --retry-delay 2 -o "$dest.part" "$url"
    if ($LASTEXITCODE -ne 0) { $failed += $rel; Remove-Item "$dest.part" -ErrorAction SilentlyContinue; continue }

    if ((Get-Item "$dest.part").Length -ne $f.bytes) {
        $failed += "$rel (size mismatch)"
        Remove-Item "$dest.part" -ErrorAction SilentlyContinue
        continue
    }
    Move-Item -LiteralPath "$dest.part" -Destination $dest -Force
    $ok++
}

Write-Host ""
Write-Host "downloaded : $ok"
Write-Host "already had: $skipped"
if ($failed.Count) {
    Write-Host "FAILED     : $($failed.Count)" -ForegroundColor Red
    $failed | ForEach-Object { Write-Host "   $_" -ForegroundColor Red }
    Write-Host "re-run this script to retry only what failed."
    exit 1
}

Write-Host "backup complete -> $Destination" -ForegroundColor Green

if ($Verify) {
    $bad = @()
    foreach ($f in $list.files) {
        $dest = Join-Path $Destination ($f.dest -replace '/', '\')
        if (-not (Test-Path -LiteralPath $dest)) { $bad += "$($f.dest) MISSING"; continue }
        if ((Get-FileHash -LiteralPath $dest -Algorithm SHA256).Hash.ToLower() -ne $f.sha256) {
            $bad += "$($f.dest) DIFFERS"
        }
    }
    if ($bad.Count) { Write-Host "VERIFY FAILED:" -ForegroundColor Red; $bad | ForEach-Object { Write-Host "   $_" }; exit 1 }
    Write-Host "verified: all $($list.files.Count) files match their recorded sha256" -ForegroundColor Green
}
