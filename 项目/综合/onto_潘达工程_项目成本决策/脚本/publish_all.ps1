# 潘达工程项目成本决策本体 - 脚本发布脚本
# 空间ID: space__panda_construction_005
# 执行方式: .\scripts\dazi.ps1 onto script publish "<此脚本路径>" --space space__panda_construction_005 --register-function-id <id>

$SPACE_ID = "space__panda_construction_005"
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=== 潘达工程本体脚本发布 ===" -ForegroundColor Cyan
Write-Host "Space ID: $SPACE_ID" -ForegroundColor Gray
Write-Host ""

# ============================================================================
# 1. 发布函数脚本（8个）
# ============================================================================
Write-Host "[1/2] 发布函数脚本..." -ForegroundColor Yellow

$functions = @(
    @{
        script = "functions\panda_fn_project_summary.py"
        function_id = "panda.fn.project_summary"
        display = "项目汇总函数"
    },
    @{
        script = "functions\panda_fn_cost_analysis.py"
        function_id = "panda.fn.cost_analysis"
        display = "成本分析函数"
    },
    @{
        script = "functions\panda_fn_risk_diagnosis.py"
        function_id = "panda.fn.risk_diagnosis"
        display = "风险诊断函数"
    },
    @{
        script = "functions\panda_fn_warning_projects.py"
        function_id = "panda.fn.warning_projects"
        display = "预警项目函数"
    },
    @{
        script = "functions\panda_fn_profit_trend.py"
        function_id = "panda.fn.profit_trend"
        display = "利润趋势函数"
    },
    @{
        script = "functions\panda_fn_collection_forecast.py"
        function_id = "panda.fn.collection_forecast"
        display = "回款预测函数"
    },
    @{
        script = "functions\panda_fn_project_comparison.py"
        function_id = "panda.fn.project_comparison"
        display = "项目对比函数"
    },
    @{
        script = "functions\panda_fn_large_customer_analysis.py"
        function_id = "panda.fn.large_customer_analysis"
        display = "大客户分析函数"
    }
)

foreach ($fn in $functions) {
    $scriptPath = Join-Path $SCRIPT_DIR $fn.script
    Write-Host "  Publishing $($fn.display)..." -NoNewline
    Write-Host " [$($fn.function_id)]" -ForegroundColor Gray

    & "$SCRIPT_DIR\..\..\..\scripts\dazi.ps1" onto script publish $scriptPath `
        --space $SPACE_ID `
        --register-function-id $fn.function_id

    if ($LASTEXITCODE -eq 0) {
        Write-Host " OK" -ForegroundColor Green
    } else {
        Write-Host " FAILED" -ForegroundColor Red
    }
}

# ============================================================================
# 2. 发布Action脚本（5个）
# ============================================================================
Write-Host ""
Write-Host "[2/2] 发布Action脚本..." -ForegroundColor Yellow

$actions = @(
    @{
        script = "actions\panda_action_update_output.py"
        action_id = "panda.action.update_output"
        permission_tag = "finance.write"
        display = "更新产值Action"
    },
    @{
        script = "actions\panda_action_update_cost.py"
        action_id = "panda.action.update_cost"
        permission_tag = "finance.write"
        display = "更新成本Action"
    },
    @{
        script = "actions\panda_action_confirm_payment.py"
        action_id = "panda.action.confirm_payment"
        permission_tag = "finance.write"
        display = "确认收款Action"
    },
    @{
        script = "actions\panda_action_trigger_warning.py"
        action_id = "panda.action.trigger_warning"
        permission_tag = "finance.write"
        display = "触发预警Action"
    },
    @{
        script = "actions\panda_action_generate_report.py"
        action_id = "panda.action.generate_report"
        permission_tag = "finance.write"
        display = "生成报表Action"
    }
)

foreach ($action in $actions) {
    $scriptPath = Join-Path $SCRIPT_DIR $action.script
    Write-Host "  Publishing $($action.display)..." -NoNewline
    Write-Host " [$($action.action_id)]" -ForegroundColor Gray

    & "$SCRIPT_DIR\..\..\..\scripts\dazi.ps1" onto script publish $scriptPath `
        --space $SPACE_ID `
        --register-action-id $action.action_id `
        --register-action-permission-tag $action.permission_tag

    if ($LASTEXITCODE -eq 0) {
        Write-Host " OK" -ForegroundColor Green
    } else {
        Write-Host " FAILED" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "=== 发布完成 ===" -ForegroundColor Cyan
Write-Host "Functions: $($functions.Count)" -ForegroundColor Gray
Write-Host "Actions: $($actions.Count)" -ForegroundColor Gray
