@set PYTHONPATH=%~dp0\pypl;%PYTHONPATH%
@set PATH=%~dp0\pypl;%PATH%

@echo To run only the fast examples, type "execfile('Examples/execall.py')"
@echo To run all the examples, type "fast=False; execfile('Examples/execall.py')"

@C:\python27\python.exe
pause
