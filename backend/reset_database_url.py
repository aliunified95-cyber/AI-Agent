"""
Reset and properly encode DATABASE_URL
This script will help you set up the DATABASE_URL correctly
"""
import os
from urllib.parse import quote_plus

env_path = os.path.join(os.path.dirname(__file__), '.env')

print("=" * 60)
print("DATABASE_URL Setup Helper")
print("=" * 60)
print("\nYour Supabase connection string template:")
print("postgresql://postgres:[YOUR_PASSWORD]@db.jdewgrtmhrvzimbtfeqs.supabase.co:5432/postgres")
print("\n" + "=" * 60)

# Get password from user
print("\nPlease enter your Supabase database password:")
print("(The password will be URL-encoded automatically)")
password = input("Password: ").strip()

if not password:
    print("ERROR: Password cannot be empty!")
    exit(1)

# URL encode the password (encode all special characters)
encoded_password = quote_plus(password, safe='')

# Construct the full URL
database_url = f"postgresql://postgres:{encoded_password}@db.jdewgrtmhrvzimbtfeqs.supabase.co:5432/postgres"

print(f"\nEncoded password: {encoded_password[:30]}...")
print(f"\nFull DATABASE_URL: {database_url[:60]}...")

# Read existing .env file
if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        lines = f.readlines()
else:
    print("ERROR: .env file not found!")
    exit(1)

# Update DATABASE_URL
new_lines = []
updated = False

for line in lines:
    if line.startswith('DATABASE_URL='):
        new_lines.append(f'DATABASE_URL={database_url}\n')
        updated = True
    else:
        new_lines.append(line)

# If DATABASE_URL wasn't found, add it
if not updated:
    # Find a good place to add it (after API keys)
    insert_index = len(new_lines)
    for i, line in enumerate(new_lines):
        if line.startswith('# Application') or line.startswith('APP_ENV'):
            insert_index = i
            break
    new_lines.insert(insert_index, f'\n# Database\nDATABASE_URL={database_url}\n')

# Write back
with open(env_path, 'w') as f:
    f.writelines(new_lines)

print("\n" + "=" * 60)
print("SUCCESS: DATABASE_URL has been updated!")
print("=" * 60)
print("\nYou can now run: python init_database.py")

