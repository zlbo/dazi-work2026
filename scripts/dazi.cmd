@echo off
REM 搭子 v3 CLI 包装（CMD）。转发到 PowerShell 脚本统一解析逻辑。
setlocal
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0dazi.ps1" %*
exit /b %ERRORLEVEL%
