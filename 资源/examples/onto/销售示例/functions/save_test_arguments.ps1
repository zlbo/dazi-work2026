# save_test_arguments.ps1
# 批量保存各函数的 test_arguments
# 用法：在 dazi-work 根目录执行 .\项目\<业务>\本体\ontos\<实现>\functions\save_test_arguments.ps1

$spaceId = "space__misc_01"

$functions = @(
    @{fn_id="sales.fn.get_summary"; file="sales.fn.get_summary.json"},
    @{fn_id="sales.fn.yoy_analysis"; file="sales.fn.yoy_analysis.json"},
    @{fn_id="sales.fn.mom_analysis"; file="sales.fn.mom_analysis.json"},
    @{fn_id="sales.fn.top_products"; file="sales.fn.top_products.json"},
    @{fn_id="sales.fn.customer_segmentation"; file="sales.fn.customer_segmentation.json"},
    @{fn_id="sales.fn.region_breakdown"; file="sales.fn.region_breakdown.json"},
    @{fn_id="sales.fn.channel_mix"; file="sales.fn.channel_mix.json"}
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
