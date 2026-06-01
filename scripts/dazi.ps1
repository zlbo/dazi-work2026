param(
  [Parameter(ValueFromRemainingArguments = $true)]
  [string[]]$Args
)

$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "dazi-cli-common.ps1")

if (-not $env:DAZI_WORKSPACE_ROOT) {
  $env:DAZI_WORKSPACE_ROOT = Get-DaziWorkspaceRoot
}

$cliDir = Resolve-DaziBundledCliDir -WorkspaceRoot $env:DAZI_WORKSPACE_ROOT
if (-not $cliDir) {
  Write-DaziCliNotFoundHelp -WorkspaceRoot $env:DAZI_WORKSPACE_ROOT
  exit 2
}

$env:DAZI_BUNDLED_DIR = $cliDir
$daziJs = Join-Path $cliDir "dazi.js"

Push-Location $env:DAZI_WORKSPACE_ROOT
try {
  & node $daziJs @Args
  exit $LASTEXITCODE
} finally {
  Pop-Location
}
