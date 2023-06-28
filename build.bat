@echo off
mode con: cols=120 lines=30
color 08
title Build
cls

title Building...

timeout /t 2 /NOBREAK >nul

python --version 2>&1 | findstr /C:" 3.11" >nul
if %errorlevel% neq 0 (
    echo Python 3.11 is not installed or not in path.
    color 0c
    pause
    color 07
    title Command Prompt
    exit /b
)


git --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0c
    echo Git is not installed or not in path.
    pause
    color 07
    title Command Prompt
    exit /b
)
echo.
cd venv\scripts
pip install -r requirements.txt
cd ..\..
cls

color 07

choice /c:YN /n /m "? build qrcode utility? (Y/n)"
if %errorlevel% equ 2 (
    echo Exiting builder...
    timeout /t 1 /NOBREAK >nul
    exit /b
)

py -3.11 builder.py

echo.
pause
title Command Prompt
color 07
