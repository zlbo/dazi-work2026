# 批量保存各函数的 test_arguments
# 用法：在 dazi-work 根目录执行 .\项目\DAZI_TEST\本体\ontos\设备运营\functions\save_test_arguments.ps1

$spaceId = "space_cate_test01"

$functions = @(
    @{ fn_id = "equip_ops.fn.get_summary"; file = "equip_ops.fn.get_summary.json" },
    @{ fn_id = "equip_ops.fn.oee_analysis"; file = "equip_ops.fn.oee_analysis.json" },
    @{ fn_id = "equip_ops.fn.availability_analysis"; file = "equip_ops.fn.availability_analysis.json" },
    @{ fn_id = "equip_ops.fn.downtime_breakdown"; file = "equip_ops.fn.downtime_breakdown.json" },
    @{ fn_id = "equip_ops.fn.yoy_analysis"; file = "equip_ops.fn.yoy_analysis.json" },
    @{ fn_id = "equip_ops.fn.mom_analysis"; file = "equip_ops.fn.mom_analysis.json" },
    @{ fn_id = "equip_ops.fn.top_fault_equipment"; file = "equip_ops.fn.top_fault_equipment.json" },
    @{ fn_id = "equip_ops.fn.maintenance_compliance"; file = "equip_ops.fn.maintenance_compliance.json" },
    @{ fn_id = "equip_ops.fn.energy_intensity"; file = "equip_ops.fn.energy_intensity.json" },
    @{ fn_id = "equip_ops.fn.plan_vs_actual"; file = "equip_ops.fn.plan_vs_actual.json" },
    @{ fn_id = "equip_ops.fn.unit_comparison"; file = "equip_ops.fn.unit_comparison.json" }
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
