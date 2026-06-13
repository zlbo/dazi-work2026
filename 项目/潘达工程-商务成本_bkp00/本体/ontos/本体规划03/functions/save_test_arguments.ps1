# 批量保存各函数的 test_arguments（V3）
# 用法：在 dazi-work 根目录执行 .\项目\潘达工程-商务成本\本体\ontos\本体规划03\functions\save_test_arguments.ps1

$spaceId = "space__panda_construction"

$functions = @(
    @{ fn_id = "panda_cost.fn.get_summary"; file = "panda_cost.fn.get_summary.json" },
    @{ fn_id = "panda_cost.fn.profit_analysis"; file = "panda_cost.fn.profit_analysis.json" },
    @{ fn_id = "panda_cost.fn.output_analysis"; file = "panda_cost.fn.output_analysis.json" },
    @{ fn_id = "panda_cost.fn.cost_structure"; file = "panda_cost.fn.cost_structure.json" },
    @{ fn_id = "panda_cost.fn.payment_analysis"; file = "panda_cost.fn.payment_analysis.json" },
    @{ fn_id = "panda_cost.fn.balance_breakdown"; file = "panda_cost.fn.balance_breakdown.json" },
    @{ fn_id = "panda_cost.fn.yoy_analysis"; file = "panda_cost.fn.yoy_analysis.json" },
    @{ fn_id = "panda_cost.fn.mom_analysis"; file = "panda_cost.fn.mom_analysis.json" },
    @{ fn_id = "panda_cost.fn.indicator_status"; file = "panda_cost.fn.indicator_status.json" },
    @{ fn_id = "panda_cost.fn.risk_overview"; file = "panda_cost.fn.risk_overview.json" },
    @{ fn_id = "panda_cost.fn.company_comparison"; file = "panda_cost.fn.company_comparison.json" },
    @{ fn_id = "panda_cost.fn.region_comparison"; file = "panda_cost.fn.region_comparison.json" },
    @{ fn_id = "panda_cost.fn.top_risk_projects"; file = "panda_cost.fn.top_risk_projects.json" },
    @{ fn_id = "panda_cost.fn.project_health"; file = "panda_cost.fn.project_health.json" }
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
        & dazi onto function save-test-arguments $ofnId --space $spaceId --arguments-json-file $jsonPath
    } else {
        Write-Host "函数 $fnId 未找到，请先 publish"
    }
}

Write-Host "完成"
