@echo off
echo Installing backend dependencies...
echo.
echo Step 1: Upgrading pip, setuptools, and wheel...
python -m pip install --upgrade pip setuptools wheel
echo.
echo Step 2: Installing requirements...
pip install -r requirements.txt
echo.
echo Installation complete!
pause

