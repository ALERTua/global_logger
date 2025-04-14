
@echo off
call %~dp0\constants.cmd

echo Generating Sphinx API documentation
sphinx-apidoc -f -o="%~dp0source" "%~dp0../global_logger" "**/tryouts*"
echo Done generating Sphinx API documentation
