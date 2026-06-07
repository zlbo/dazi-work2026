# save_test_arguments.ps1
# 批量保存各函数的 test_arguments
# 用法：在 dazi-work 根目录执行 .\项目\DAZI_TEST\本体\ontos\利润分析示例\functions\save_test_arguments.ps1

$spaceId = "space__misc_01"

$functions = @(
    @{fn_id="profit.fn.get_summary"; file="profit.fn.get_summary.json"},
    @{fn_id="profit.fn.yoy_analysis"; file="profit.fn.yoy_analysis.json"},
    @{fn_id="profit.fn.mom_analysis"; file="profit.fn.mom_analysis.json"},
    @{fn_id="profit.fn.budget_vs_actual"; file="profit.fn.budget_vs_actual.json"},
    @{fn_id="profit.fn.account_breakdown"; file="profit.fn.account_breakdown.json"},
    @{fn_id="profit.fn.cost_center_profit"; file="profit.fn.cost_center_profit.json"},
    @{fn_id="profit.fn.top_accounts"; file="profit.fn.top_accounts.json"}
)

Write-Host "获取函数列表..."
$fnListRaw = & dazi onto function list --space $spaceId --json 2>&1
$jsonLines = ($fnListRaw | Where-Object { $_ -notmatch '__JSON_SUMMARY__' }) -join "`n"
$fnList = $jsonLines | ConvertFrom-Json

foreach ($fn in $functions) {
    $fnId = $fn.fn_id
    $fileName = $fn.file
    $jsonPath = "$PSScriptRoot/test_arguments/$fileName"

    if (-not (Test-Path $jsonPath)) {
        Write-Host "跳过 $fnId：找不到 $jsonPath"
        continue
    }

    Write-Host "保存 $fnId ..."
    & dazi onto function save-test-arguments --function-id $fnId --space $spaceId --arguments-json-file $jsonPath
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  ✗ 保存失败" -ForegroundColor Red
    }
}

Write-Host "完成"
