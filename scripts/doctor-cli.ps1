# dazi v3 CLI doctor (dazi-work + vsix only, no source repo)
# Usage: .\scripts\doctor-cli.ps1

param(
  [switch]$Json,
  [switch]$SkipAuth
)

$ErrorActionPreference = "Continue"
. (Join-Path $PSScriptRoot "dazi-cli-common.ps1")

$wsRoot = Get-DaziWorkspaceRoot
$checks = New-Object System.Collections.Generic.List[object]
$script:fail = 0
$script:warn = 0

function Add-Check {
  param(
    [string]$Id,
    [string]$Name,
    [ValidateSet("ok", "warn", "fail")]
    [string]$Status,
    [string]$Detail = "",
    [string]$Fix = ""
  )
  if ($Status -eq "fail") { $script:fail++ }
  if ($Status -eq "warn") { $script:warn++ }
  $checks.Add([PSCustomObject]@{
      id     = $Id
      name   = $Name
      status = $Status
      detail = $Detail
      fix    = $Fix
    }) | Out-Null
}

function Write-StatusIcon {
  param([string]$s)
  if ($s -eq "ok") { return "[OK]" }
  if ($s -eq "warn") { return "[!!]" }
  return "[XX]"
}

# Node
$nodeCmd = Get-Command node -ErrorAction SilentlyContinue
if (-not $nodeCmd) {
  Add-Check -Id "node" -Name "Node.js" -Status "fail" -Detail "node not found" -Fix "Install Node.js 18+"
} else {
  $verLine = (& node -v 2>&1 | Out-String).Trim()
  $major = 0
  if ($verLine -match "v(\d+)") { $major = [int]$Matches[1] }
  if ($major -ge 18) {
    Add-Check -Id "node" -Name "Node.js" -Status "ok" -Detail "$verLine @ $($nodeCmd.Source)"
  } else {
    Add-Check -Id "node" -Name "Node.js" -Status "warn" -Detail "$verLine (need >= 18)" -Fix "Upgrade Node.js"
  }
}

Add-Check -Id "workspace" -Name "dazi-work root" -Status "ok" -Detail $wsRoot

$runtimeApps = Get-DaziRuntimeAppsRoot -WorkspaceRoot $wsRoot
if ($runtimeApps) {
  Add-Check -Id "runtime-apps" -Name "runtime-apps" -Status "ok" -Detail $runtimeApps
} else {
  Add-Check -Id "runtime-apps" -Name "runtime-apps" -Status "warn" `
    -Detail "missing templates/ + sdk/" `
    -Fix "Keep dazi-work/runtime-apps complete or set DAZI_RUNTIME_APPS_ROOT"
}

$candidates = Get-DaziBundledCliCandidates -WorkspaceRoot $wsRoot
$cliDir = Resolve-DaziBundledCliDir -WorkspaceRoot $wsRoot
$resolvedSource = $null
$idx = 0

foreach ($c in $candidates) {
  $idx++
  $st = if ($c.Ok) { "ok" } else { "warn" }
  $detail = $c.Path
  if ($c.Note) { $detail = "$detail | $($c.Note)" }
  Add-Check -Id "cli-cand-$idx" -Name "CLI candidate: $($c.Source)" -Status $st -Detail $detail
  if ($c.Ok -and -not $resolvedSource) { $resolvedSource = $c.Source }
}

$cliNames = @("dazi.js", "dazi-onto.js", "dazi-flow.js", "dazi-app.js")
if ($cliDir) {
  Add-Check -Id "cli-resolved" -Name "bundled CLI resolved" -Status "ok" `
    -Detail "$cliDir | source: $resolvedSource"
  foreach ($f in $cliNames) {
    $fp = Join-Path $cliDir $f
    if (Test-Path $fp) {
      Add-Check -Id "file-$f" -Name $f -Status "ok" -Detail $fp
    } else {
      Add-Check -Id "file-$f" -Name $f -Status "fail" -Detail "missing $fp" `
        -Fix "Copy full bundled/clis (4 js files)"
    }
  }
  $daziJs = Join-Path $cliDir "dazi.js"
  $v = (& node $daziJs --version 2>&1 | Select-Object -Last 1)
  if ($LASTEXITCODE -eq 0) {
    Add-Check -Id "cli-version" -Name "dazi --version" -Status "ok" -Detail ([string]$v).Trim()
  } else {
    Add-Check -Id "cli-version" -Name "dazi --version" -Status "fail" -Detail ([string]$v)
  }
} else {
  $fixMsg = @"
Install dazitech.dazi-vscode vsix in Trae/Cursor/VS Code (see .trae / .cursor / .vscode extensions),
OR: .\scripts\sync-clis-from-extension.ps1
OR: copy bundled/clis to $wsRoot\tools\dazi-clis
OR: set DAZI_BUNDLED_DIR
"@
  Add-Check -Id "cli-resolved" -Name "bundled CLI resolved" -Status "fail" -Detail "dazi.js not found" -Fix $fixMsg
  foreach ($f in $cliNames) {
    Add-Check -Id "file-$f" -Name $f -Status "fail" -Detail "skipped"
  }
}

$authPath = Join-Path $env:USERPROFILE ".dazi\auth.json"
$legacyAuth = Join-Path $env:USERPROFILE ".dazi-app\auth.json"
if (Test-Path $authPath) {
  Add-Check -Id "auth" -Name "auth file" -Status "ok" -Detail $authPath
} elseif (Test-Path $legacyAuth) {
  Add-Check -Id "auth" -Name "auth file" -Status "warn" -Detail "legacy only: $legacyAuth" `
    -Fix "Run .\scripts\dazi.ps1 auth login"
} else {
  Add-Check -Id "auth" -Name "auth file" -Status "warn" -Detail "not logged in" `
    -Fix ".\scripts\dazi.ps1 auth login"
}

if (-not $SkipAuth -and $cliDir -and (Test-Path $authPath)) {
  $env:DAZI_BUNDLED_DIR = $cliDir
  Push-Location $wsRoot
  try {
    $out = & node (Join-Path $cliDir "dazi.js") auth whoami 2>&1
    if ($LASTEXITCODE -eq 0) {
      $line = ($out | Where-Object { $_ -and $_ -notmatch "__JSON_SUMMARY__" } | Select-Object -Last 1)
      Add-Check -Id "auth-whoami" -Name "dazi auth whoami" -Status "ok" -Detail ([string]$line)
    } else {
      Add-Check -Id "auth-whoami" -Name "dazi auth whoami" -Status "warn" `
        -Detail (($out | Select-Object -Last 2) -join " | ") `
        -Fix "Check token expiry and serverUrl"
    }
  } catch {
    Add-Check -Id "auth-whoami" -Name "dazi auth whoami" -Status "warn" -Detail $_.Exception.Message
  } finally {
    Pop-Location
  }
}

if ($runtimeApps) {
  $appEntry = Resolve-DaziAppCliEntry -RuntimeAppsRoot $runtimeApps -BundledCliDir $cliDir
  if ($appEntry) {
    Add-Check -Id "dazi-app" -Name "dazi-app entry" -Status "ok" `
      -Detail "$($appEntry.Path) ($($appEntry.Source))"
    if (-not $appEntry.IsLauncher) {
      $av = (& node $appEntry.Path --version 2>&1 | Select-Object -Last 1)
      if ($LASTEXITCODE -eq 0) {
        Add-Check -Id "dazi-app-version" -Name "dazi-app --version" -Status "ok" -Detail ([string]$av).Trim()
      } else {
        Add-Check -Id "dazi-app-version" -Name "dazi-app --version" -Status "fail" -Detail ([string]$av)
      }
    } else {
      $pnpm = Get-Command pnpm -ErrorAction SilentlyContinue
      if ($pnpm) {
        Push-Location $runtimeApps
        try {
          $env:DAZI_APP_CLI_SOURCE = "quiet"
          if ($cliDir) { $env:DAZI_BUNDLED_DIR = $cliDir }
          $av = (& pnpm run dazi-app -- --version 2>&1 | Select-Object -Last 1)
          if ($LASTEXITCODE -eq 0) {
            Add-Check -Id "dazi-app-version" -Name "pnpm dazi-app --version" -Status "ok" -Detail ([string]$av).Trim()
          } else {
            Add-Check -Id "dazi-app-version" -Name "pnpm dazi-app --version" -Status "fail" -Detail ([string]$av)
          }
        } finally {
          Pop-Location
        }
      } else {
        Add-Check -Id "dazi-app-version" -Name "pnpm dazi-app" -Status "warn" -Detail "pnpm not found" `
          -Fix "Install pnpm for frontend workflow"
      }
    }
  } else {
    Add-Check -Id "dazi-app" -Name "dazi-app entry" -Status "fail" `
      -Detail "dazi-app.js / launcher not found" `
      -Fix "Install vsix or copy dazi-app.js to tools/dazi-clis"
  }
}

if ($Json) {
  [PSCustomObject]@{
    ok     = ($script:fail -eq 0)
    fail   = $script:fail
    warn   = $script:warn
    checks = $checks
  } | ConvertTo-Json -Depth 5
  if ($script:fail -gt 0) { exit 2 }
  if ($script:warn -gt 0) { exit 1 }
  exit 0
}

Write-Host ""
Write-Host "Dazi v3 CLI doctor" -ForegroundColor Cyan
Write-Host "Workspace: $wsRoot"
Write-Host ("-" * 60)

foreach ($c in $checks) {
  $icon = Write-StatusIcon $c.status
  $color = "Green"
  if ($c.status -eq "warn") { $color = "Yellow" }
  if ($c.status -eq "fail") { $color = "Red" }
  Write-Host "$icon $($c.name)" -ForegroundColor $color
  if ($c.detail) { Write-Host "     $($c.detail)" -ForegroundColor DarkGray }
  if ($c.fix -and $c.status -ne "ok") { Write-Host "     fix: $($c.fix)" -ForegroundColor DarkYellow }
}

Write-Host ("-" * 60)
if ($script:fail -eq 0 -and $script:warn -eq 0) {
  Write-Host "Ready. Try: .\scripts\dazi.ps1 onto function list --space <id>" -ForegroundColor Green
} elseif ($script:fail -gt 0) {
  Write-Host "Fix [XX] items before using CLI." -ForegroundColor Red
} else {
  Write-Host "CLI usable with warnings." -ForegroundColor Yellow
}
Write-Host "Summary: $($checks.Count) checks | fail=$($script:fail) warn=$($script:warn)"
Write-Host ""

if ($script:fail -gt 0) { exit 2 }
if ($script:warn -gt 0) { exit 1 }
exit 0
