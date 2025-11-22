"""
Fix DATABASE_URL by URL-encoding the password
"""
import os
from urllib.parse import quote_plus

env_path = os.path.join(os.path.dirname(__file__), '.env')

if not os.path.exists(env_path):
    print("ERROR: .env file not found!")
    exit(1)

# Read .env file
with open(env_path, 'r') as f:
    lines = f.readlines()

# Fix DATABASE_URL
new_lines = []
updated = False

for line in lines:
    if line.startswith('DATABASE_URL='):
        # Extract the URL
        db_url = line.split('=', 1)[1].strip()
        
        # Parse and encode password
        if '://' in db_url and '@' in db_url:
            parts = db_url.split('://')
            scheme = parts[0]
            rest = parts[1]
            
            if '@' in rest:
                user_pass, host_db = rest.split('@', 1)
                if ':' in user_pass:
                    user, password = user_pass.split(':', 1)
                    # URL encode the password (quote_plus handles @, +, etc.)
                    # But we need to be careful - if password already has @, we need to encode it
                    # First, check if there are multiple @ signs
                    if password.count('@') > 0:
                        # The password contains @, encode it
                        encoded_password = quote_plus(password, safe='')
                    else:
                        encoded_password = quote_plus(password)
                    # Reconstruct URL
                    fixed_url = f"{scheme}://{user}:{encoded_password}@{host_db}"
                    new_lines.append(f'DATABASE_URL={fixed_url}\n')
                    updated = True
                    print(f"Fixed DATABASE_URL - password has been URL-encoded")
                    print(f"Original password: {password[:20]}...")
                    print(f"Encoded password: {encoded_password[:20]}...")
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

if updated:
    # Write back
    with open(env_path, 'w') as f:
        f.writelines(new_lines)
    print("\nSUCCESS: DATABASE_URL has been fixed!")
    print("The password special characters have been URL-encoded.")
else:
    print("No changes needed.")

