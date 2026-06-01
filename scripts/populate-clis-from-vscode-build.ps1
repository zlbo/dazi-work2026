# 从 dazi-vscode 构建产物同步 CLI 到 tools/dazi-clis（发版/交付用）
# Usage: .\scripts\populate-clis-from-vscode-build.ps1 [-VsixRepoRoot "D:\src2025\ads2025\dazi\dazi-vscode"]

param(
  [string]$VsixRepoRoot = ""
)

$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "dazi-cli-common.ps1")

$wsRoot = Get-DaziWorkspaceRoot
$dest = Join-Path $wsRoot "tools\dazi-clis"

if (-not $VsixRepoRoot) {
  # 默认：dazi-work 的上级为 ads2025，其下 dazi/dazi-vscode
  $guess = Join-Path (Split-Path $wsRoot -Parent) "dazi\dazi-vscode"
  if (Test-Path (Join-Path $guess "package.json")) {
    $VsixRepoRoot = $guess
  }
}

if (-not $VsixRepoRoot -or -not (Test-Path $VsixRepoRoot)) {
  Write-Error "Set -VsixRepoRoot to dazi-vscode repo (with bundled/clis after pnpm run bundle:clis)"
}

$src = Join-Path $VsixRepoRoot "bundled\clis"
if (-not (Test-Path (Join-Path $src "dazi.js"))) {
  Write-Host "Missing $src\dazi.js — run in dazi-vscode:" -ForegroundColor Yellow
  Write-Host "  pnpm run bundle:clis"
  exit 1
}

New-Item -ItemType Directory -Path $dest -Force | Out-Null
foreach ($f in @("dazi.js", "dazi-onto.js", "dazi-flow.js", "dazi-app.js")) {
  Copy-Item (Join-Path $src $f) (Join-Path $dest $f) -Force
  Write-Host "copied $f"
}

Write-Host ""
Write-Host "Done -> $dest" -ForegroundColor Green
Write-Host "Verify: .\scripts\dazi.ps1 --version"
