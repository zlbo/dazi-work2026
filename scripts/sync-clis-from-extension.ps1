# 从已安装的 dazi-vscode 扩展复制 bundled/clis 到 dazi-work/tools/dazi-clis
# Usage: .\scripts\sync-clis-from-extension.ps1

$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "dazi-cli-common.ps1")

$wsRoot = Get-DaziWorkspaceRoot
$dest = Join-Path $wsRoot "tools\dazi-clis"
$srcDir = $null

foreach ($c in (Get-DaziBundledCliCandidates -WorkspaceRoot $wsRoot)) {
  if ($c.Source -match "extension|trae|cursor|vscode" -and $c.Ok) {
    $srcDir = $c.Path
    break
  }
}

if (-not $srcDir) {
  Write-Error @"
No bundled/clis with dazi.js found.
Install dazi-vscode.vsix in Trae/Cursor/VS Code, then rerun.
Or set DAZI_BUNDLED_DIR to an existing bundled/clis folder.
Searched: Trae (.trae/extensions), Cursor, VS Code, VSCODE_EXTENSIONS.
"@
}

if (-not (Test-Path $dest)) {
  New-Item -ItemType Directory -Path $dest -Force | Out-Null
}

$files = @("dazi.js", "dazi-onto.js", "dazi-flow.js", "dazi-app.js")
foreach ($f in $files) {
  $from = Join-Path $srcDir $f
  if (-not (Test-Path $from)) {
    Write-Warning "skip missing: $from"
    continue
  }
  Copy-Item -Path $from -Destination (Join-Path $dest $f) -Force
  Write-Host "copied $f"
}

Write-Host ""
Write-Host "Done -> $dest" -ForegroundColor Green
Write-Host "Verify: .\scripts\dazi.ps1 --version"
