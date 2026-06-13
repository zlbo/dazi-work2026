# 批量保存 profit01 函数 test_arguments
# 用法：在 dazi-work 根目录执行
#   .\项目\DAZI_TEST\本体\ontos\利润分析01\functions\save_test_arguments.ps1

$spaceId = "space__onto_engine_test"

$functions = @(
    @{ fn_id = "profit01.fn.get_summary"; file = "profit01.fn.get_summary.json" },
    @{ fn_id = "profit01.fn.project_profit"; file = "profit01.fn.project_profit.json" },
    @{ fn_id = "profit01.fn.account_breakdown"; file = "profit01.fn.account_breakdown.json" },
    @{ fn_id = "profit01.fn.cost_type_breakdown"; file = "profit01.fn.cost_type_breakdown.json" },
    @{ fn_id = "profit01.fn.budget_vs_actual"; file = "profit01.fn.budget_vs_actual.json" },
    @{ fn_id = "profit01.fn.region_profit"; file = "profit01.fn.region_profit.json" },
    @{ fn_id = "profit01.fn.org_profit"; file = "profit01.fn.org_profit.json" }
)

foreach ($fn in $functions) {
    $jsonPath = Join-Path $PSScriptRoot "test_arguments/$($fn.file)"
    if (-not (Test-Path $jsonPath)) {
        Write-Host "跳过 $($fn.fn_id)：找不到 $jsonPath"
        continue
    }
    Write-Host "保存 $($fn.fn_id) ..."
    & dazi onto function save-test-arguments --function-id $fn.fn_id --space $spaceId --arguments-json-file $jsonPath
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  保存失败" -ForegroundColor Red
    }
}

Write-Host "完成"
