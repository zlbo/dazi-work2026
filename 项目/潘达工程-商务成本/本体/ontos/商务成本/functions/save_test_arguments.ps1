# 批量保存测试参数脚本
# 用法：.\\save_test_arguments.ps1 -space <space-id>

param(
    [Parameter(Mandatory=$true)]
    [string]$space
)

$functionIds = @(
    "commercial_cost.fn.get_summary",
    "commercial_cost.fn.trend_analysis",
    "commercial_cost.fn.mom_analysis",
    "commercial_cost.fn.yoy_analysis",
    "commercial_cost.fn.structure_analysis",
    "commercial_cost.fn.cost_composition",
    "commercial_cost.fn.plan_vs_actual",
    "commercial_cost.fn.org_analysis",
    "commercial_cost.fn.region_analysis",
    "commercial_cost.fn.risk_analysis",
    "commercial_cost.fn.financial_health"
)

$basePath = ".\test_arguments"

foreach ($functionId in $functionIds) {
    $jsonFile = "$basePath\$functionId.json"
    
    if (Test-Path $jsonFile) {
        Write-Host "Saving test arguments for $functionId..."
        dazi onto function save-test-arguments `
            --function-id $functionId `
            --space $space `
            --arguments-json-file $jsonFile
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Successfully saved test arguments for $functionId`n"
        } else {
            Write-Host "❌ Failed to save test arguments for $functionId`n"
        }
    } else {
        Write-Host "⚠️  JSON file not found: $jsonFile`n"
    }
}

Write-Host "`n🎉 Batch save completed!"