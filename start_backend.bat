@echo off
echo Starting Zain AI Voice Agent Backend...
cd /d "%~dp0backend"
if exist venv\Scripts\Activate.bat (
    call venv\Scripts\Activate.bat
) else (
    echo Virtual environment not found. Please run install_dependencies.bat first.
    pause
    exit /b 1
)
python run.py
pause

