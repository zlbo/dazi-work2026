# 批量保存各函数的 test_arguments
# 用法：在 dazi-work 根目录执行 .\项目\DAZI_TEST\本体\ontos\生产计划\functions\save_test_arguments.ps1

$spaceId = "space_cate_test01"

$functions = @(
    @{ fn_id = "prod_plan.fn.get_summary"; file = "prod_plan.fn.get_summary.json" },
    @{ fn_id = "prod_plan.fn.plan_vs_actual"; file = "prod_plan.fn.plan_vs_actual.json" },
    @{ fn_id = "prod_plan.fn.work_order_status"; file = "prod_plan.fn.work_order_status.json" },
    @{ fn_id = "prod_plan.fn.capacity_load"; file = "prod_plan.fn.capacity_load.json" },
    @{ fn_id = "prod_plan.fn.material_shortage"; file = "prod_plan.fn.material_shortage.json" },
    @{ fn_id = "prod_plan.fn.product_mix"; file = "prod_plan.fn.product_mix.json" },
    @{ fn_id = "prod_plan.fn.yoy_analysis"; file = "prod_plan.fn.yoy_analysis.json" },
    @{ fn_id = "prod_plan.fn.mom_analysis"; file = "prod_plan.fn.mom_analysis.json" },
    @{ fn_id = "prod_plan.fn.top_delayed_orders"; file = "prod_plan.fn.top_delayed_orders.json" },
    @{ fn_id = "prod_plan.fn.line_comparison"; file = "prod_plan.fn.line_comparison.json" }
)

Write-Host "获取函数列表..."
$raw = (dazi onto function list --space $spaceId 2>&1) -join "`n"
$idx = $raw.IndexOf('__JSON_SUMMARY__')
if ($idx -lt 0) {
    Write-Host "无法解析 function list 输出"
    exit 1
}
$fnList = ($raw.Substring($idx + 16) | ConvertFrom-Json).data.functions

foreach ($fn in $functions) {
    $fnId = $fn.fn_id
    $jsonPath = Join-Path $PSScriptRoot "test_arguments/$($fn.file)"
    $fnInfo = $fnList | Where-Object { $_.function_id -eq $fnId }
    if ($fnInfo) {
        $ofnId = $fnInfo.id
        Write-Host "保存 $fnId (ofnId=$ofnId)..."
        & dazi onto function save-test-arguments --function-id $fnId --space $spaceId --arguments-json-file $jsonPath
    } else {
        Write-Host "函数 $fnId 未找到，请先 publish"
    }
}

Write-Host "完成"
