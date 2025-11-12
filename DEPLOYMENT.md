# Deployment Guide

## Quick Deploy Options

### Option 1: Railway (Recommended - Easiest) ⭐

Railway provides both PostgreSQL database and app hosting in one platform with automatic GitHub deployments.

#### Step 1: Push to GitHub

```bash
# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Car Repair Shop Mock API"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/car-repair-api.git
git branch -M main
git push -u origin main
```

#### Step 2: Deploy to Railway

1. **Sign up at [Railway](https://railway.app/)**
   - Use your GitHub account for easier integration

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `car-repair-api` repository

3. **Add PostgreSQL Database**
   - In your project dashboard, click "+ New"
   - Select "Database" → "Add PostgreSQL"
   - Railway will automatically create the database

4. **Configure Environment Variables**
   - Click on your app service
   - Go to "Variables" tab
   - Railway auto-adds `DATABASE_URL` from PostgreSQL
   - Add these additional variables:
     ```
     SECRET_KEY=<generate-random-string>
     ADMIN_API_KEY=<your-admin-key>
     ENVIRONMENT=production
     DEBUG=false
     CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
     ```

5. **Deploy**
   - Railway automatically deploys on push
   - Wait for deployment to complete
   - You'll get a public URL like: `https://your-app.railway.app`

6. **Seed the Database**
   - In Railway dashboard, click on your app
   - Go to "Settings" → "Deploy"
   - In the logs, you can run:
   ```bash
   railway run python -m app.seed_data
   ```
   OR use Railway CLI (see below)

#### Using Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Seed the database
railway run python -m app.seed_data

# View logs
railway logs
```

**Your API will be live at:** `https://your-app.railway.app/docs`

**Cost:** Free tier includes:
- $5 of usage per month
- 500 hours of usage
- Enough for a demo/development API

---

### Option 2: Render (Also Easy, Similar to Railway)

Render also provides both database and app hosting.

#### Step 1: Push to GitHub (same as above)

#### Step 2: Deploy to Render

1. **Sign up at [Render](https://render.com/)**

2. **Create PostgreSQL Database**
   - Dashboard → New → PostgreSQL
   - Choose free tier
   - Note the connection details

3. **Create Web Service**
   - Dashboard → New → Web Service
   - Connect your GitHub repository
   - Settings:
     - **Name:** car-repair-api
     - **Environment:** Docker
     - **Region:** Choose closest to you
     - **Instance Type:** Free

4. **Set Environment Variables**
   ```
   DATABASE_URL=<from-postgresql-service>
   SECRET_KEY=<generate-random-string>
   ADMIN_API_KEY=<your-admin-key>
   ENVIRONMENT=production
   DEBUG=false
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy
   - You'll get a URL like: `https://your-app.onrender.com`

6. **Seed Database**
   - Go to your web service
   - Click "Shell" tab
   - Run: `python -m app.seed_data`

**Your API will be live at:** `https://your-app.onrender.com/docs`

**Cost:** Free tier includes:
- 750 hours per month
- Spins down after 15 minutes of inactivity
- 90-second boot time on first request

---

### Option 3: Supabase (DB) + Railway/Render (App)

Use Supabase for the database (with extra features) and Railway/Render for the app.

#### Step 1: Set up Supabase Database

1. **Sign up at [Supabase](https://supabase.com/)**

2. **Create New Project**
   - Organization → New Project
   - Choose free tier
   - Set a strong database password

3. **Get Connection String**
   - Project Settings → Database
   - Connection String → URI
   - Copy the connection string (looks like):
     ```
     postgresql://postgres:[YOUR-PASSWORD]@db.xxx.supabase.co:5432/postgres
     ```

#### Step 2: Deploy App to Railway or Render

Follow Option 1 or 2 above, but use the Supabase connection string for `DATABASE_URL`

**Benefits of Supabase:**
- Built-in admin dashboard
- Automatic API generation
- Real-time subscriptions
- Authentication features
- Storage for files
- Row-level security

**Cost:** Free tier includes:
- 500 MB database
- 2 GB bandwidth
- Good for development/small projects

---

## After Deployment Checklist

1. **✅ Seed the Database**
   ```bash
   # Railway
   railway run python -m app.seed_data

   # Render
   # Use the Shell tab in dashboard
   python -m app.seed_data
   ```

2. **✅ Test API Endpoints**
   ```bash
   curl -H "X-API-Key: test-key-1234567890" \
     https://your-app.railway.app/api/v1/customers
   ```

3. **✅ Create New API Keys**
   ```bash
   curl -X POST \
     -H "X-API-Key: YOUR_ADMIN_KEY" \
     -H "Content-Type: application/json" \
     -d '{"name":"Production API Key"}' \
     https://your-app.railway.app/api/v1/admin/api-keys
   ```

4. **✅ Update CORS Origins**
   - Add your frontend domains to `CORS_ORIGINS` environment variable

5. **✅ Set Up Custom Domain (Optional)**
   - Railway: Settings → Domains → Add custom domain
   - Render: Settings → Custom Domain

6. **✅ Monitor Usage**
   - Check Railway/Render dashboard for usage stats
   - Set up alerts for quota limits

---

## Environment Variables Reference

Required environment variables for production:

```bash
# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Security (generate strong random strings)
SECRET_KEY=your-secret-key-min-32-chars
ADMIN_API_KEY=your-admin-api-key

# Application
PROJECT_NAME=Car Repair Shop Mock API
VERSION=1.0.0
API_V1_PREFIX=/api/v1
ENVIRONMENT=production
DEBUG=false

# CORS (comma-separated)
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Optional
DEFAULT_PAGE_SIZE=20
MAX_PAGE_SIZE=100
```

### Generate Secure Keys

```bash
# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate ADMIN_API_KEY
python -c "import uuid; print(str(uuid.uuid4()))"
```

---

## Troubleshooting

### Database Connection Issues

```bash
# Test database connection
python -c "from app.database import engine; engine.connect(); print('✓ Connected')"
```

### Check Logs

```bash
# Railway
railway logs

# Render
# Use Logs tab in dashboard
```

### Port Issues

Railway and Render automatically set the `PORT` environment variable. The app should bind to `0.0.0.0:$PORT`.

If you need to customize, update the Dockerfile CMD:
```dockerfile
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
```

---

## Cost Comparison

| Provider | Free Tier | Database | Best For |
|----------|-----------|----------|----------|
| **Railway** | $5 credit/month | ✅ PostgreSQL | Easiest setup |
| **Render** | 750 hrs/month | ✅ PostgreSQL | Free static sites |
| **Supabase** | 500 MB database | ✅ PostgreSQL | Backend features |
| **Fly.io** | 3 VMs free | ❌ (paid) | Global deployment |

---

## Next Steps

1. **Documentation**: Share your API docs URL (`/docs`)
2. **API Keys**: Generate and distribute API keys to users
3. **Monitoring**: Set up error tracking (Sentry, etc.)
4. **Rate Limiting**: Consider adding rate limiting for production
5. **Backup**: Set up database backups (most platforms do this automatically)
6. **Analytics**: Track API usage with tools like PostHog or Mixpanel

---

## Support

- **Railway**: https://railway.app/help
- **Render**: https://render.com/docs
- **Supabase**: https://supabase.com/docs

Your API will be publicly accessible at your deployment URL with full Swagger documentation! 🚀
