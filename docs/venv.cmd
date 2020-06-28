
@echo off
call %~dp0constants.cmd

set _verbose_venv=
if defined verbose if not defined nointeractive set _verbose_venv=-i

call %VENV_ACTIVATE%
    %VENV_PYTHON% %_verbose_venv% %*
call %VENV_DEACTIVATE%
