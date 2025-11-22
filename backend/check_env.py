"""
Check and fix DATABASE_URL in .env file
"""
import os
from urllib.parse import quote_plus

env_path = os.path.join(os.path.dirname(__file__), '.env')

if not os.path.exists(env_path):
    print("ERROR: .env file not found!")
    exit(1)

# Read .env file
with open(env_path, 'r') as f:
    content = f.read()

# Check DATABASE_URL
if 'DATABASE_URL' in content:
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('DATABASE_URL='):
            db_url = line.split('=', 1)[1].strip()
            print(f"Current DATABASE_URL: {db_url[:50]}...")
            
            if '[YOUR_PASSWORD]' in db_url:
                print("\nERROR: You still need to replace [YOUR_PASSWORD] with your actual password!")
                print("\nTo fix:")
                print("1. Open backend/.env file")
                print("2. Find the DATABASE_URL line")
                print("3. Replace [YOUR_PASSWORD] with your actual Supabase password")
                print("4. If your password has special characters, they may need to be URL-encoded")
                exit(1)
            else:
                # Check if password needs encoding
                if '@' in db_url and '://' in db_url:
                    parts = db_url.split('://')
                    if len(parts) == 2:
                        scheme = parts[0]
                        rest = parts[1]
                        if '@' in rest:
                            user_pass, host_db = rest.split('@', 1)
                            if ':' in user_pass:
                                user, password = user_pass.split(':', 1)
                                # Check if password has special characters
                                if any(c in password for c in ['@', '#', '$', '%', '&', '+', '=', '?', '/']):
                                    print("\nWARNING: Your password contains special characters that may need URL encoding.")
                                    print("If connection fails, try URL-encoding your password.")
                                    print(f"Example: If password is 'pass@word', use 'pass%40word'")
                print("\nDATABASE_URL looks correct. Trying to connect...")
                break
else:
    print("ERROR: DATABASE_URL not found in .env file!")
    exit(1)

