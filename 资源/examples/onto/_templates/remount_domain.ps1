# remount_domain.ps1 — 本体域成员补挂模板
# 复制到 项目/<业务>/本体/ontos/<实现>/setup/ 并修改 $spaceId、$itemRel、$functions
#
# 用法（dazi-work 根）：
#   .\项目\<业务>\本体\ontos\<实现>\setup\<name>_remount_domain.ps1

param(
    [switch]$SkipFunctions,
    [switch]$FunctionsOnly
)

$ErrorActionPreference = "Stop"

$spaceId = "space__YOUR_SPACE"
$itemRel = "项目/<业务名>/本体/ontos/<实现名>"
$categoryMountRel = "$itemRel/setup/<prefix>_category_mount.py"

$functions = @(
    @{ rel = "$itemRel/functions/<prefix>_fn_example.py"; id = "<domain>.fn.example"; cat = "总览分析" }
)

Write-Host "=== 本体域成员补挂 ===" -ForegroundColor Cyan
& dazi auth whoami
if ($LASTEXITCODE -ne 0) { exit 1 }

& dazi onto domain ensure --onto-dir $itemRel
if ($LASTEXITCODE -ne 0) { exit 1 }

if (-not $FunctionsOnly) {
    & dazi onto script publish $categoryMountRel --space $spaceId --type setup
    if ($LASTEXITCODE -ne 0) { exit 1 }
    & dazi onto script run --file $categoryMountRel --space $spaceId
    if ($LASTEXITCODE -ne 0) { exit 1 }
}

if (-not $SkipFunctions) {
    foreach ($fn in $functions) {
        & dazi onto script publish $fn.rel `
            --space $spaceId `
            --register-function-id $fn.id `
            --register-platform-category $fn.cat `
            --mount-domain auto
        if ($LASTEXITCODE -ne 0) { exit 1 }
    }
}

& dazi onto domain show --onto-dir $itemRel
Write-Host "=== 完成 ===" -ForegroundColor Green
