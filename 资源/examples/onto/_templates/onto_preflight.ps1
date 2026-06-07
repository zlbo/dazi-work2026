# onto_preflight.ps1 — 本体实施门禁（规划 ↔ 函数文件 ↔ 平台注册）
# 用法（在 dazi-work 根目录）：
#   .\项目\<业务>\本体\ontos\<实现>\functions\onto_preflight.ps1
# 或复制到 functions/ 后修改下方 $spaceId、$itemRel

param(
    [string]$SpaceId = "space__misc_01",
    [string]$ItemRel = "项目/DAZI_TEST/本体/ontos/销售本体示例"
)

$ErrorActionPreference = "Stop"
$functionsDir = Join-Path $PSScriptRoot "."
$plansDir = Join-Path (Split-Path $PSScriptRoot -Parent) "plans"

Write-Host "=== 本体 preflight ===" -ForegroundColor Cyan
Write-Host "空间: $SpaceId"
Write-Host "实现: $ItemRel"

$exitCode = 0

# 1. functions/*.py 数量
$pyFiles = @(Get-ChildItem -Path $functionsDir -Filter "*.py" -File | Where-Object { $_.Name -notmatch "^_" })
$pyCount = $pyFiles.Count
Write-Host "`n[1] functions/*.py 数量: $pyCount"

# 2. 平台 function list
Write-Host "[2] 拉取 function list ..."
$fnListRaw = & dazi onto function list --space $SpaceId --json 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ✗ function list 失败" -ForegroundColor Red
    exit 1
}
# 去掉 __JSON_SUMMARY__ 行后解析
$jsonLines = ($fnListRaw | Where-Object { $_ -notmatch '__JSON_SUMMARY__' }) -join "`n"
$fnList = $jsonLines | ConvertFrom-Json
$listCount = @($fnList).Count
Write-Host "  平台已注册: $listCount"

if ($pyCount -ne $listCount) {
    Write-Host "  ✗ 文件数 ($pyCount) ≠ 平台注册数 ($listCount)" -ForegroundColor Red
    $exitCode = 1
} else {
    Write-Host "  ✓ 文件数与平台注册数一致" -ForegroundColor Green
}

# 3. 规划函数表行数（粗略：plans/*.md 中含 .fn. 的行）
$planFnCount = 0
if (Test-Path $plansDir) {
    $planFiles = Get-ChildItem -Path $plansDir -Filter "*.md" -File
    foreach ($pf in $planFiles) {
        $content = Get-Content $pf.FullName -Raw -Encoding UTF8
        $matches = [regex]::Matches($content, '\w+\.fn\.\w+')
        $planFnCount += $matches.Count
    }
}
if ($planFnCount -gt 0) {
    Write-Host "`n[3] plans 中 .fn. 引用约: $planFnCount"
    if ($planFnCount -ne $pyCount) {
        Write-Host "  ⚠ 规划引用数 ($planFnCount) ≠ functions/*.py ($pyCount)" -ForegroundColor Yellow
    } else {
        Write-Host "  ✓ 与 functions/*.py 数量一致" -ForegroundColor Green
    }
} else {
    Write-Host "`n[3] 跳过 plans 计数（无 plans/*.md 或未找到 .fn.）" -ForegroundColor Yellow
}

# 4. 本地 publish-preview 静态预检（每个函数）
Write-Host "`n[4] 本体函数 publish-preview 静态预检 ..."
foreach ($py in $pyFiles) {
    $rel = "$ItemRel/functions/$($py.Name)"
    Write-Host "  → $($py.Name)"
    & dazi onto script publish-preview $rel --space $SpaceId 2>&1 | Out-Host
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  ✗ $($py.Name) 预检失败" -ForegroundColor Red
        $exitCode = 1
    }
}

if ($exitCode -eq 0) {
    Write-Host "`n=== preflight 通过 ===" -ForegroundColor Green
} else {
    Write-Host "`n=== preflight 未通过 ===" -ForegroundColor Red
}
exit $exitCode
