
@echo off
call %~dp0constants.cmd

call %VENV_PIP% install sphinx sphinx-rtd-theme
call %~dp0_sphinx-apidoc.cmd
call %~dp0_make.bat html
start "" "%~dp0build\\html\\index.html"
exit /b
