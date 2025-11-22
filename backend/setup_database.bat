@echo off
echo Setting up database connection...
echo.
echo Step 1: Make sure you've updated the DATABASE_URL in .env file
echo         Replace [YOUR_PASSWORD] with your actual Supabase password
echo.
pause
echo.
echo Step 2: Installing database dependencies...
pip install sqlalchemy psycopg2-binary alembic
echo.
echo Step 3: Creating database tables...
python init_database.py
echo.
echo Database setup complete!
pause

