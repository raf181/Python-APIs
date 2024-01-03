@echo off
setlocal

REM Install Python if not already installed
python --version 2>nul
if %errorlevel% neq 0 (
    echo Installing Python...
    REM You can replace the link below with the latest Python version
    curl -o python-installer.exe https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python-installer.exe
) else (
    echo Python is already installed.
)

REM Install required Python packages
echo Installing required Python packages...
pip install flask
pip install Flask-BasicAuth
echo.
echo.
echo Dependencies installation completed.
echo.
pause