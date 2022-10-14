@echo off
For %%A in ("%~dp0.") do set SCRIPT_DIR=%%~dpA
Echo "CREATING PYTHON VENV python_env_playwright"
python -m venv %HOMEDRIVE%%HOMEPATH%\python_env
Echo set PYTHONPATH=%SCRIPT_DIR% >> %HOMEDRIVE%%HOMEPATH%\python_env_playwright\Scripts\activate.bat
Echo set MYPYPATH=%SCRIPT_DIR% >> %HOMEDRIVE%%HOMEPATH%\python_env_playwright\Scripts\activate.bat
Echo "SOURCING VENV"
call %HOMEDRIVE%%HOMEPATH%\python_env_playwright\Scripts\activate.bat
Echo "UPGRADING PIP"
python -m pip install --upgrade pip
Echo "INSTALLING PACKAGES"
pip install --no-cache-dir -r %SCRIPT_DIR%\scripts\requirements.txt
