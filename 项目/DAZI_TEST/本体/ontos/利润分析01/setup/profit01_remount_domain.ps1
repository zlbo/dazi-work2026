# 利润分析01 — 本体域成员补挂（bulk + 函数 publish 入域）
#
# 适用：已跑过 init/seed/函数 publish，但管理端本体域树 table/object/cube 仍为灰色。
#
# 用法（dazi-work 根目录）：
#   .\项目\DAZI_TEST\本体\ontos\利润分析01\setup\profit01_remount_domain.ps1
#   .\项目\DAZI_TEST\本体\ontos\利润分析01\setup\profit01_remount_domain.ps1 -SkipFunctions
#   .\项目\DAZI_TEST\本体\ontos\利润分析01\setup\profit01_remount_domain.ps1 -FunctionsOnly

param(
    [switch]$SkipFunctions,
    [switch]$FunctionsOnly
)

$ErrorActionPreference = "Stop"

$spaceId = "space__onto_engine_test"
$itemRel = "项目/DAZI_TEST/本体/ontos/利润分析01"
$setupRel = "$itemRel/setup/profit01_category_mount.py"

$functions = @(
    @{ rel = "$itemRel/functions/profit01_fn_get_summary.py"; id = "profit01.fn.get_summary"; cat = "总览分析" },
    @{ rel = "$itemRel/functions/profit01_fn_project_profit.py"; id = "profit01.fn.project_profit"; cat = "结构分析" },
    @{ rel = "$itemRel/functions/profit01_fn_account_breakdown.py"; id = "profit01.fn.account_breakdown"; cat = "结构分析" },
    @{ rel = "$itemRel/functions/profit01_fn_cost_type_breakdown.py"; id = "profit01.fn.cost_type_breakdown"; cat = "结构分析" },
    @{ rel = "$itemRel/functions/profit01_fn_budget_vs_actual.py"; id = "profit01.fn.budget_vs_actual"; cat = "预实分析" },
    @{ rel = "$itemRel/functions/profit01_fn_region_profit.py"; id = "profit01.fn.region_profit"; cat = "组织分析" },
    @{ rel = "$itemRel/functions/profit01_fn_org_profit.py"; id = "profit01.fn.org_profit"; cat = "组织分析" }
)

Write-Host "=== 利润分析01 · 本体域成员补挂 ===" -ForegroundColor Cyan
Write-Host "空间: $spaceId"
Write-Host "实现: $itemRel"
Write-Host ""

& dazi auth whoami
if ($LASTEXITCODE -ne 0) {
    Write-Host "请先 dazi auth login" -ForegroundColor Red
    exit 1
}

Write-Host "[0] 确认本体域实体 ..." -ForegroundColor Yellow
& dazi onto domain ensure --onto-dir $itemRel
if ($LASTEXITCODE -ne 0) { exit 1 }

if (-not $FunctionsOnly) {
    Write-Host "`n[1] 发布并执行 category_mount（平台分类 + s.domain.apply_registry）..." -ForegroundColor Yellow
    & dazi onto script publish $setupRel --space $spaceId --type setup
    if ($LASTEXITCODE -ne 0) { exit 1 }
    & dazi onto script run --file $setupRel --space $spaceId
    if ($LASTEXITCODE -ne 0) { exit 1 }
}

if (-not $SkipFunctions) {
    Write-Host "`n[2] 重发布全部函数（--mount-domain auto 入域 script+function）..." -ForegroundColor Yellow
    foreach ($fn in $functions) {
        Write-Host "  → $($fn.id)" -ForegroundColor Gray
        & dazi onto script publish $fn.rel `
            --space $spaceId `
            --register-function-id $fn.id `
            --register-platform-category $fn.cat `
            --mount-domain auto
        if ($LASTEXITCODE -ne 0) {
            Write-Host "  ✗ 发布失败: $($fn.id)" -ForegroundColor Red
            exit 1
        }
    }
}

Write-Host "`n[3] 域树验收 ..." -ForegroundColor Yellow
& dazi onto domain show --onto-dir $itemRel
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ⚠ domain show 失败，请在管理端打开本体域详情核对 kind count" -ForegroundColor Yellow
    exit 0
}

Write-Host "`n=== 完成 ===" -ForegroundColor Green
Write-Host "请在管理端「本体域 → 利润分析01」确认 table/object/cube/function count > 0"
