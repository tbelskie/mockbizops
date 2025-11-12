# Deploying Your Documentation Website

This guide explains how to get your API documentation site live at `mockbizops.com`.

## What You Have

You now have **TWO separate things**:

### 1. API Backend (Railway)
- **Location:** `app/` folder
- **What it does:** The actual API that returns data
- **Deploy to:** Railway (see `QUICKSTART.md`)
- **URL:** `https://your-app.up.railway.app`

### 2. Documentation Website (docs-site/)
- **Location:** `docs-site/` folder
- **What it does:** Teaches developers how to use your API
- **Deploy to:** GitHub Pages, Netlify, Vercel, etc.
- **URL:** `mockbizops.com` (your choice)

## Two-Step Deployment

### Step 1: Deploy API Backend to Railway

```bash
# From project root
./setup_deployment.sh  # Generate keys
git add .
git commit -m "Initial commit"
git push to GitHub
# Deploy to Railway (see QUICKSTART.md)
```

**Result:** API running at `https://your-app.up.railway.app`

### Step 2: Deploy Docs Site

#### Option A: GitHub Pages (Recommended)

**Create separate repo for docs:**

```bash
cd docs-site

# Initialize new repo
git init
git add .
git commit -m "Initial commit: API documentation"

# Create new GitHub repo called "mockbizops-docs"
git remote add origin https://github.com/YOUR_USERNAME/mockbizops-docs.git
git branch -M main
git push -u origin main

# Enable GitHub Pages:
# Go to: Settings → Pages
# Source: main branch, / (root)
# Save
```

**Your docs will be at:** `https://YOUR_USERNAME.github.io/mockbizops-docs/`

#### Option B: Netlify (Easiest Custom Domain)

```bash
cd docs-site

# Method 1: Drag & Drop
# Go to https://app.netlify.com/drop
# Drag the docs-site folder
# Done!

# Method 2: CLI
npm install -g netlify-cli
netlify deploy --prod
```

**Your docs will be at:** `https://random-name.netlify.app`

#### Option C: Vercel

```bash
cd docs-site

npm install -g vercel
vercel --prod
```

## Connect Custom Domain

### Buy Domain

Go to:
- Namecheap.com
- Domains.google.com
- Cloudflare Registrar
- GoDaddy

Search for `mockbizops.com` and purchase (~$12/year)

### Configure DNS

#### For GitHub Pages:

1. **Add CNAME file to your repo:**
   ```bash
   echo "mockbizops.com" > CNAME
   git add CNAME
   git commit -m "Add custom domain"
   git push
   ```

2. **Configure DNS at your domain registrar:**
   ```
   Type: A
   Name: @
   Value: 185.199.108.153
          185.199.109.153
          185.199.110.153
          185.199.111.153

   Type: CNAME
   Name: www
   Value: YOUR_USERNAME.github.io
   ```

3. **Wait 10-30 minutes** for DNS propagation

4. **Visit:** `https://mockbizops.com` ✅

#### For Netlify:

1. **In Netlify Dashboard:**
   - Go to Site settings → Domain management
   - Click "Add custom domain"
   - Enter `mockbizops.com`

2. **Follow Netlify's DNS instructions**
   - They'll show you exactly what records to add
   - Usually a CNAME pointing to your Netlify subdomain

3. **Wait 10-30 minutes**

4. **Visit:** `https://mockbizops.com` ✅

#### For Vercel:

1. **In Vercel Dashboard:**
   - Project Settings → Domains
   - Add `mockbizops.com`

2. **Configure DNS as instructed**

3. **Wait 10-30 minutes**

## Update Configuration

After deploying both parts, update the docs site with your real API URL:

### 1. Update Base URL

**In `docs-site/playground.html`:**
```html
<!-- Change this -->
<input type="text" id="baseUrl" value="https://api.mockbizops.com">

<!-- To your Railway URL -->
<input type="text" id="baseUrl" value="https://your-app.up.railway.app">
```

### 2. Update Code Examples

**In `docs-site/docs.html`:**

Find all instances of:
```
https://api.mockbizops.com
```

Replace with:
```
https://your-app.up.railway.app
```

### 3. Update Test Key

**In `docs-site/playground.html`:**
```html
<input type="text" id="apiKey" value="YOUR-ACTUAL-TEST-KEY">
```

### 4. Commit and Push

```bash
git add .
git commit -m "Update API URLs"
git push
```

Your site will update automatically!

## Complete Setup Checklist

- [ ] **Deploy API to Railway**
  - [ ] Push code to GitHub
  - [ ] Deploy on Railway
  - [ ] Add PostgreSQL database
  - [ ] Set environment variables
  - [ ] Seed database
  - [ ] Test API: `curl https://your-app.up.railway.app/health`

- [ ] **Deploy Docs Site**
  - [ ] Choose hosting (GitHub Pages recommended)
  - [ ] Push docs-site to repo
  - [ ] Enable hosting
  - [ ] Test site loads

- [ ] **Configure Custom Domain**
  - [ ] Buy domain (mockbizops.com)
  - [ ] Add DNS records
  - [ ] Wait for propagation
  - [ ] Test: `https://mockbizops.com`

- [ ] **Update Configuration**
  - [ ] Update API URLs in docs
  - [ ] Update test API key
  - [ ] Test playground works
  - [ ] Test code examples

- [ ] **Polish**
  - [ ] Add your branding/logo
  - [ ] Customize colors
  - [ ] Add analytics (optional)
  - [ ] Add more examples

## Final Architecture

```
                         Internet
                            │
                ┌───────────┴───────────┐
                │                       │
                ▼                       ▼
    ┌─────────────────────┐  ┌─────────────────────┐
    │  mockbizops.com     │  │  Railway Backend    │
    │  (Docs Website)     │  │  API Endpoints      │
    │                     │  │                     │
    │  GitHub Pages/      │  │  PostgreSQL DB      │
    │  Netlify/Vercel     │  │  Mock Data          │
    └─────────────────────┘  └─────────────────────┘
             │                         ▲
             │                         │
             │  Developers read docs   │
             │  See examples           │
             │  Test in playground     │
             │                         │
             └─────API Requests────────┘
```

## Examples of What You Get

### Homepage
```
https://mockbizops.com/
→ Landing page with features, pricing, quick start
```

### Documentation
```
https://mockbizops.com/docs.html
→ Getting started guide with code examples
```

### API Reference
```
https://mockbizops.com/api-reference.html
→ Detailed endpoint documentation
```

### Interactive Playground
```
https://mockbizops.com/playground.html
→ Test API calls in browser
```

## Maintenance

### Update Documentation

```bash
# Edit files locally
cd docs-site
# Make changes
git add .
git commit -m "Update documentation"
git push

# Site updates automatically!
```

### Update API

```bash
# API changes are separate
cd ..  # back to project root
# Make changes to app/ folder
git push

# Railway redeploys automatically
```

## Costs

### API Backend (Railway)
- **Free Tier:** $5 credit/month (~500 hours)
- **Paid:** ~$5-20/month depending on usage

### Documentation Website
- **GitHub Pages:** FREE
- **Netlify:** FREE (100GB bandwidth)
- **Vercel:** FREE (100GB bandwidth)
- **Cloudflare Pages:** FREE (unlimited bandwidth)

### Domain
- **mockbizops.com:** $10-15/year

### Total Estimate
- **Development/Testing:** FREE (test with Railway free tier)
- **Production:** $10-15/year (domain) + $5-20/month (Railway)

## Troubleshooting

### Docs site not loading
- Check DNS propagation: https://dnschecker.org
- Verify deployment succeeded in hosting dashboard
- Check for typos in domain configuration

### API not responding from playground
- Check Railway deployment is running
- Verify API URL is correct in playground
- Check CORS settings in Railway:
  ```
  CORS_ORIGINS=https://mockbizops.com
  ```

### Custom domain not working
- DNS can take 24-48 hours (usually 10-30 minutes)
- Verify all DNS records are correct
- Check hosting provider's domain settings

## Next Steps

1. **Add more content:**
   - Write tutorials
   - Add use cases
   - Create video guides

2. **Improve SEO:**
   - Add meta tags
   - Submit to Google Search Console
   - Create sitemap

3. **Add features:**
   - Blog for updates
   - Status page
   - Community forum

4. **Promote:**
   - Share on Twitter/LinkedIn
   - Post on Product Hunt
   - Write blog posts

---

**You now have a complete, professional API product!** 🚀

- ✅ Production API backend
- ✅ Professional documentation website
- ✅ Custom domain
- ✅ Interactive playground
- ✅ Code examples
- ✅ Developer-friendly

Share it with the world! 🌎
