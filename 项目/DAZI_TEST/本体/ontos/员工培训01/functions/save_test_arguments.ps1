# 批量保存 training01 函数 test_arguments
# 用法：在 dazi-work 根目录执行
#   .\项目\DAZI_TEST\本体\ontos\员工培训01\functions\save_test_arguments.ps1

$spaceId = "space__onto_engine_test"

$functions = @(
    @{ fn_id = "training01.fn.get_summary"; file = "training01.fn.get_summary.json" },
    @{ fn_id = "training01.fn.org_breakdown"; file = "training01.fn.org_breakdown.json" },
    @{ fn_id = "training01.fn.category_breakdown"; file = "training01.fn.category_breakdown.json" },
    @{ fn_id = "training01.fn.top_courses"; file = "training01.fn.top_courses.json" },
    @{ fn_id = "training01.fn.plan_vs_actual"; file = "training01.fn.plan_vs_actual.json" },
    @{ fn_id = "training01.fn.compliance_status"; file = "training01.fn.compliance_status.json" },
    @{ fn_id = "training01.fn.coverage_analysis"; file = "training01.fn.coverage_analysis.json" }
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
