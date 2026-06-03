param(
  [Parameter(ValueFromRemainingArguments = $true)]
  [string[]]$Args
)

$ErrorActionPreference = "Stop"

# 自动处理执行策略问题
try {
  # 检查当前执行策略
  $currentPolicy = Get-ExecutionPolicy -Scope Process -ErrorAction SilentlyContinue
  if (-not $currentPolicy -or $currentPolicy -eq "Restricted") {
    # 临时设置执行策略为 RemoteSigned（仅当前进程有效）
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned -Force -ErrorAction SilentlyContinue | Out-Null
  }
} catch {
  # 如果设置失败，继续执行，可能会在后面失败，但至少尝试了
}

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