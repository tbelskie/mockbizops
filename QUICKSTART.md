# 🚀 Quick Start - Deploy in 5 Minutes

Get your Car Repair Shop Mock API live on the internet in just a few steps!

## Step 1: Prepare for Deployment (1 minute)

Run the setup script to generate secure keys:

```bash
./setup_deployment.sh
```

This will generate:
- `SECRET_KEY` (for security)
- `ADMIN_API_KEY` (for admin endpoints)

**Save these keys!** You'll need them in Step 3.

## Step 2: Push to GitHub (2 minutes)

### Create GitHub Repository

1. Go to https://github.com/new
2. Name it: `car-repair-api`
3. Keep it **Public** (for easy deployment) or Private if you prefer
4. **Don't** initialize with README (we already have one)
5. Click "Create repository"

### Push Your Code

```bash
# Add all files
git add .

# Commit
git commit -m "Initial commit: Car Repair Shop Mock API"

# Add GitHub remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/car-repair-api.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Deploy to Railway (2 minutes)

### Sign Up & Deploy

1. **Go to [Railway.app](https://railway.app/)** and sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `car-repair-api`
   - Click "Deploy Now"

3. **Add Database**
   - Click "+ New" in your project
   - Select "Database" → "Add PostgreSQL"
   - Railway will automatically create it

4. **Set Environment Variables**
   - Click on your app service (not the database)
   - Go to "Variables" tab
   - Railway automatically adds `DATABASE_URL`
   - Click "New Variable" and add each of these:

   ```
   Variable Name: SECRET_KEY
   Value: [paste from setup script]

   Variable Name: ADMIN_API_KEY
   Value: [paste from setup script]

   Variable Name: ENVIRONMENT
   Value: production

   Variable Name: DEBUG
   Value: false

   Variable Name: CORS_ORIGINS
   Value: *
   ```

5. **Redeploy** (if needed)
   - Click "Deploy" → "Redeploy"

6. **Get Your URL**
   - Go to "Settings" → "Domains"
   - You'll see something like: `car-repair-api-production-xxxx.up.railway.app`
   - Click "Generate Domain" if not auto-generated

## Step 4: Seed the Database

Install Railway CLI:

```bash
# macOS/Linux
brew install railway

# OR with npm
npm install -g @railway/cli
```

Link and seed:

```bash
# Login
railway login

# Link to your project
railway link

# Seed the database
railway run python -m app.seed_data
```

**Alternative** (without CLI):
- Go to your app service in Railway dashboard
- Click on "Deployments" tab
- Click on the latest deployment
- Use the "View Logs" to see when it's ready
- You can also add a one-time job to seed data

## ✅ You're Live!

Your API is now publicly accessible at:

```
https://your-app-name.up.railway.app/docs
```

### Test It Out

```bash
# Replace with your actual Railway URL
curl -H "X-API-Key: test-key-1234567890" \
  https://your-app.up.railway.app/api/v1/customers
```

### Test API Keys (after seeding)

- `test-key-1234567890`
- `demo-key-abcdefghij`

### Share Your API

Send users to your Swagger docs:
```
https://your-app.up.railway.app/docs
```

---

## Troubleshooting

### "Application failed to start"

Check logs in Railway dashboard. Common issues:
- Database not connected (check `DATABASE_URL` variable)
- Missing environment variables

### "Can't connect to database"

- Make sure PostgreSQL service is running in Railway
- Check that `DATABASE_URL` is automatically set
- Wait 1-2 minutes for database to initialize

### "No data returned"

- Database needs to be seeded
- Run: `railway run python -m app.seed_data`

### Want to add a custom domain?

1. Railway Settings → Domains
2. Add custom domain
3. Update your DNS records as shown
4. Update `CORS_ORIGINS` if needed

---

## Next Steps

1. **Share your API**: Send the `/docs` URL to users
2. **Create API keys**: Use admin endpoints to create new keys
3. **Monitor usage**: Check Railway dashboard for metrics
4. **Set up alerts**: Railway can notify you of issues
5. **Add custom domain**: Professional look with your own domain

---

## Cost

**Railway Free Tier:**
- $5 credit per month
- ~500 hours of usage
- Perfect for demo/development
- No credit card required initially

**When you need more:**
- Upgrade to Railway Pro ($20/month)
- Or migrate to another platform

---

## Need Help?

- **Detailed Guide**: See `DEPLOYMENT.md`
- **Railway Docs**: https://docs.railway.app
- **API Docs**: https://your-app.up.railway.app/docs

**Congratulations! Your API is live! 🎉**
