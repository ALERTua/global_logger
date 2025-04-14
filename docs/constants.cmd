
@echo off
set PYTHONIOENCODING=UTF-8
set PYTHONWARNINGS=ignore:DEPRECATION::pip._internal.cli.base_command

set "REPO_ROOT=%~dp0../"
set "SOURCE_ROOT=%REPO_ROOT%global_logger"
set "REQUIREMENTS=%SOURCE_ROOT%\requirements.txt"

rem for %%A in ("%cd%") do set "dir_name=%%~nA"

rem set verbose=on
rem set verbose=full
if ["%verbose%"]==["full"] echo on
