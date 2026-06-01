@echo off
REM 搭子 v3 CLI 自检。用法：scripts\doctor-cli.cmd
setlocal
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0doctor-cli.ps1" %*
exit /b %ERRORLEVEL%
