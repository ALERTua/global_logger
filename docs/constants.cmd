
@echo off
set PYTHONIOENCODING=UTF-8
set PYTHONWARNINGS=ignore:DEPRECATION::pip._internal.cli.base_command

set "REPO_ROOT=%~dp0../"
set "SOURCE_ROOT=%REPO_ROOT%global_logger"
set "VENV=%~dp0venv.cmd"
set "VENV_ROOT=%REPO_ROOT%venv310"-
set "VENV_SCRIPTS=%VENV_ROOT%\Scripts"
set "VENV_PYTHON=%VENV_SCRIPTS%\python.exe"
set "VENV_PIP=%VENV_SCRIPTS%\pip.exe"
set "VENV_ACTIVATE=%VENV_SCRIPTS%\activate.bat"
set "VENV_DEACTIVATE=%VENV_SCRIPTS%\deactivate.bat"
set "REQUIREMENTS=%SOURCE_ROOT%\requirements.txt"

rem for %%A in ("%cd%") do set "dir_name=%%~nA"

rem set verbose=on
rem set verbose=full
if ["%verbose%"]==["full"] echo on
