
@echo off
pushd %~dp0
call constants.cmd

"%venv_scripts%\sphinx-apidoc.exe" -f -o="%~dp0source" "%~dp0../global_logger"
