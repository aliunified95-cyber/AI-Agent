"""
Script to create .env file with database configuration
"""
import os

env_content = """# API Keys
CLAUDE_API_KEY=[YOUR_CLAUDE_API_KEY]
ELEVENLABS_API_KEY=[YOUR_ELEVENLABS_API_KEY]
ELEVENLABS_VOICE_ID=QBygrd2fm6CyJnkw7dDn
OPENAI_API_KEY=[YOUR_OPENAI_API_KEY]

# Database
# IMPORTANT: Replace [YOUR_PASSWORD] with your actual Supabase database password
DATABASE_URL=postgresql://postgres:[YOUR_PASSWORD]@db.jdewgrtmhrvzimbtfeqs.supabase.co:5432/postgres

# Application
APP_ENV=development
DEBUG=true
LOG_LEVEL=INFO
"""

env_path = os.path.join(os.path.dirname(__file__), '.env')

# Database URL to add/update
database_url = "postgresql://postgres:[YOUR_PASSWORD]@db.jdewgrtmhrvzimbtfeqs.supabase.co:5432/postgres"

if os.path.exists(env_path):
    print(".env file already exists. Updating DATABASE_URL...")
    # Read existing content
    with open(env_path, 'r') as f:
        lines = f.readlines()
    
    # Check if DATABASE_URL exists and update it, or add it
    updated = False
    new_lines = []
    for line in lines:
        if line.startswith('DATABASE_URL='):
            new_lines.append(f'DATABASE_URL={database_url}\n')
            updated = True
        else:
            new_lines.append(line)
    
    # If DATABASE_URL wasn't found, add it
    if not updated:
        # Add after API keys section or at the end
        new_lines.append(f'\n# Database\nDATABASE_URL={database_url}\n')
    
    # Write back
    with open(env_path, 'w') as f:
        f.writelines(new_lines)
    
    print("SUCCESS: DATABASE_URL updated in .env file!")
else:
    # Create new file
    with open(env_path, 'w') as f:
        f.write(env_content)
    print("SUCCESS: .env file created successfully!")

print("\nIMPORTANT: Please edit .env file and replace [YOUR_PASSWORD] with your actual Supabase password!")

