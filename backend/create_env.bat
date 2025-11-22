@echo off
echo Creating .env file...
python create_env.py
echo.
echo Please edit the .env file and replace [YOUR_PASSWORD] with your actual Supabase password!
pause

