@echo off
setlocal

:: 设置工作区根目录
set "DAZI_WORKSPACE_ROOT=%~dp0.."

:: 设置 CLI 目录
set "DAZI_BUNDLED_DIR=%DAZI_WORKSPACE_ROOT%\tools\dazi-clis"
set "DAZI_JS=%DAZI_BUNDLED_DIR%\dazi.js"

:: 切换到工作区根目录
pushd "%DAZI_WORKSPACE_ROOT%"

:: 使用 PowerShell 的 ExecutionPolicy Bypass 来运行 node 命令
powershell -ExecutionPolicy Bypass -Command "node '%DAZI_JS%' %*"

:: 保存退出码
set "EXIT_CODE=%errorlevel%"

:: 恢复目录
popd

:: 退出
exit /b %EXIT_CODE%