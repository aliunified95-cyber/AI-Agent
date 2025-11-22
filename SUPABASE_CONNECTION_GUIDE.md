# Supabase Connection Troubleshooting Guide

## Issue: Hostname Cannot Be Resolved

The error "could not translate host name" means your computer cannot find the Supabase database server. This could be due to:

1. **Incorrect hostname** - The connection string might be wrong
2. **Network/DNS issue** - Your internet connection or DNS might be blocking it
3. **Supabase project status** - The project might be paused or deleted

## How to Get the Correct Connection String

### Step 1: Go to Supabase Dashboard

1. Log in to [https://supabase.com](https://supabase.com)
2. Select your project
3. Go to **Settings** → **Database**

### Step 2: Find Connection String

Look for **Connection string** or **Connection pooling** section. You should see something like:

```
postgresql://postgres.[PROJECT-REF]:[YOUR-PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
```

OR

```
postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
```

### Step 3: Verify Your Connection String

The format should be:
- **Host**: `db.[PROJECT-REF].supabase.co` or `aws-0-[REGION].pooler.supabase.com`
- **Port**: `5432` (direct) or `6543` (pooler)
- **Database**: `postgres`
- **User**: `postgres`

### Step 4: Update .env File

1. Copy the **exact** connection string from Supabase dashboard
2. Replace `[YOUR-PASSWORD]` with your actual database password
3. Update `backend/.env` file with the correct `DATABASE_URL`

### Step 5: Test Connection

Run the test script:

```powershell
python test_db_connection.py
```

## Alternative: Use Connection Pooler

If direct connection doesn't work, try the **Connection Pooler**:

1. In Supabase dashboard: **Settings** → **Database** → **Connection Pooling**
2. Use the **Session mode** or **Transaction mode** connection string
3. The port will be `6543` instead of `5432`

## Common Issues

### Issue: "Name or service not known"
- **Solution**: Verify the hostname is correct from Supabase dashboard
- Check if your project is active (not paused)

### Issue: "Connection refused"
- **Solution**: Check if your IP is whitelisted in Supabase
- Go to **Settings** → **Database** → **Network Restrictions**

### Issue: "Password authentication failed"
- **Solution**: Reset your database password in Supabase dashboard
- **Settings** → **Database** → **Reset Database Password**

## Quick Fix Script

After getting the correct connection string from Supabase:

```powershell
python reset_database_url.py
```

Enter your password when prompted, and it will be properly encoded.

## Still Having Issues?

1. **Check Supabase Status**: Visit [status.supabase.com](https://status.supabase.com)
2. **Verify Project**: Make sure your Supabase project is active
3. **Check Network**: Try accessing Supabase dashboard in your browser
4. **Contact Support**: If all else fails, contact Supabase support

