
@echo off
call %~dp0\constants.cmd

echo Installing sphinx and sphinx-rtd-theme
call pip install sphinx sphinx-rtd-theme toml || exit /b 1

echo Generating API documentation
call %~dp0\_sphinx-apidoc.cmd || exit /b 1

echo Building HTML documentation
call %~dp0\_make.bat html || exit /b 1

echo Opening documentation in browser
start "" "%~dp0\\build\\html\\index.html"

exit /b 0
