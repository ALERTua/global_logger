
@echo off
call %~dp0constants.cmd

call %VENV_PIP% install sphinx sphinx-rtd-theme toml || exit /b 1
call %~dp0_sphinx-apidoc.cmd || exit /b 1
call %~dp0_make.bat html || exit /b 1
start "" "%~dp0build\\html\\index.html"
exit /b 0
