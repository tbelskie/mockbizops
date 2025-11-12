# Mock BizOps Documentation Website

A professional API documentation website for the Car Repair Shop Mock API.

## What's This?

This is a **developer documentation portal** (like stripe.com/docs or twilio.com/docs) that will live at `mockbizops.com`.

**Purpose:**
- Teach developers how to use your API
- Provide code examples and guides
- Interactive API playground/tester
- NOT a data dashboard - this is for API documentation

## Structure

```
docs-site/
├── index.html          # Homepage/landing page
├── docs.html           # Getting started guide
├── api-reference.html  # API endpoint documentation
├── playground.html     # Interactive API tester
├── css/
│   └── style.css      # Stripe-inspired styling
└── js/
    └── main.js        # Interactivity
```

## Pages Overview

### 1. Homepage (index.html)
- Marketing/landing page
- Feature highlights
- Quick start guide
- Pricing tiers
- Use cases
- Endpoint preview

### 2. Documentation (docs.html)
- Getting started guide
- Authentication instructions
- Code examples (cURL, JavaScript, Python)
- Pagination, filtering, error handling
- Best practices

### 3. API Reference (api-reference.html)
- Complete endpoint documentation
- Request/response examples
- Parameters and schemas
- Status codes

### 4. Interactive Playground (playground.html)
- Test API endpoints in browser
- Configure requests
- See real responses
- Generate API keys

## Key Features

✅ **Professional Design** - Stripe-inspired, clean UI
✅ **Code Examples** - Multiple languages (cURL, JS, Python)
✅ **Interactive Playground** - Test API without writing code
✅ **Responsive** - Works on all devices
✅ **SEO Friendly** - Semantic HTML
✅ **Fast** - No dependencies, vanilla JS

## Quick Test Locally

```bash
# Just open in browser
open index.html

# Or serve with Python
python3 -m http.server 8080
# Visit: http://localhost:8080
```

## Deployment Options

### Option 1: GitHub Pages (Easiest, Free)

```bash
# Create a new repository for docs site
git init
git add .
git commit -m "Initial commit: Mock BizOps docs"

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/mockbizops-docs.git
git branch -M main
git push -u origin main

# Enable GitHub Pages:
# Settings → Pages → Source: main branch
# Your site: https://YOUR_USERNAME.github.io/mockbizops-docs
```

**Custom Domain:**
1. Add a `CNAME` file with your domain:
   ```
   mockbizops.com
   ```
2. Configure DNS:
   ```
   Type: CNAME
   Name: @
   Value: YOUR_USERNAME.github.io
   ```

### Option 2: Netlify (Also Easy, Free)

```bash
# Drag & drop the docs-site folder to netlify.com/drop
# OR connect GitHub repo
# OR use CLI:
npm install -g netlify-cli
netlify deploy --prod
```

**Custom Domain:**
1. Netlify Dashboard → Domain Settings
2. Add custom domain
3. Follow DNS instructions

### Option 3: Vercel (Great for Custom Domains)

```bash
npm install -g vercel
vercel --prod
```

### Option 4: Cloudflare Pages

1. Push to GitHub
2. Connect to Cloudflare Pages
3. Deploy automatically on push

## Configuration

### Update API URL

When you deploy your Railway backend, update the API URL in the docs:

**In playground.html:**
```html
<input type="text" id="baseUrl" value="https://your-app.up.railway.app">
```

**In docs.html and other pages:**
Replace all instances of:
```
https://api.mockbizops.com
```

With your actual API URL:
```
https://your-app.up.railway.app/api/v1
```

### Update API Key

Change the default test key in `playground.html`:
```html
<input type="text" id="apiKey" value="YOUR-TEST-KEY">
```

## Customization

### Branding

**Colors** (in `css/style.css`):
```css
:root {
    --primary: #635BFF;        /* Your brand color */
    --primary-dark: #0A2540;   /* Dark text */
    --secondary: #00D4FF;       /* Accent color */
}
```

**Logo:**
```html
<!-- In navbar -->
<div class="nav-brand">
    <img src="images/logo.png" alt="Logo" height="30">
    <h2>Your Brand Name</h2>
</div>
```

### Add More Endpoints

Update the playground dropdown:
```html
<select id="endpoint">
    <option value="/v1/your-endpoint">GET /v1/your-endpoint</option>
</select>
```

### Add More Languages

In `docs.html`, add new language tabs:
```html
<button class="language-tab" onclick="showLanguage('ruby')">Ruby</button>

<div id="ruby" class="language-content">
    <pre><code>require 'net/http'
# Your Ruby code</code></pre>
</div>
```

## Domain Setup

### Buy Domain

Options:
- Namecheap ($10-15/year)
- Google Domains ($12/year)
- Cloudflare Registrar (at-cost)
- GoDaddy

### Configure DNS

**For GitHub Pages:**
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

**For Netlify/Vercel:**
They provide specific DNS instructions in their dashboards.

## Maintenance

### Update Documentation

1. Edit the HTML files
2. Commit and push to GitHub
3. Site updates automatically (if using GitHub Pages/Netlify/Vercel)

### Add New Features

- New endpoints: Update `playground.html` dropdown
- New guides: Add sections to `docs.html`
- Blog posts: Create `blog.html`
- Examples: Add to docs or create `examples.html`

## Analytics (Optional)

### Google Analytics

Add before closing `</head>`:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

### Plausible (Privacy-friendly)

```html
<script defer data-domain="mockbizops.com" src="https://plausible.io/js/script.js"></script>
```

## SEO Optimization

Add to each page's `<head>`:

```html
<!-- SEO Meta Tags -->
<meta name="description" content="Realistic mock API for car repair shop operations. Perfect for testing and development.">
<meta name="keywords" content="mock api, test api, development api, car repair api">

<!-- Open Graph (Social Media) -->
<meta property="og:title" content="Mock BizOps - Car Repair Shop API">
<meta property="og:description" content="Production-quality mock API for testing">
<meta property="og:image" content="https://mockbizops.com/images/og-image.png">
<meta property="og:url" content="https://mockbizops.com">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Mock BizOps - Car Repair Shop API">
<meta name="twitter:description" content="Production-quality mock API">
```

## Complete Architecture

```
┌──────────────────────────────────────┐
│  mockbizops.com                      │
│  (Documentation Website)              │
│  ├── How to use the API              │
│  ├── Code examples                   │
│  ├── Interactive playground          │
│  └── Getting started guide           │
└────────────┬─────────────────────────┘
             │
             │ Users read docs
             │ Try API in playground
             ▼
┌──────────────────────────────────────┐
│  Railway Backend                     │
│  (The Actual API)                    │
│  https://your-app.up.railway.app     │
│  ├── API endpoints                   │
│  ├── PostgreSQL database             │
│  └── Mock data                       │
└──────────────────────────────────────┘
             │
             │ Developers integrate
             ▼
┌──────────────────────────────────────┐
│  Developer's Application             │
│  (Their app using your API)          │
└──────────────────────────────────────┘
```

## Next Steps

1. **Test locally** - Open `index.html` in browser
2. **Update API URLs** - Replace placeholder URLs with your Railway URL
3. **Customize branding** - Update colors, logo, company name
4. **Deploy** - Choose GitHub Pages, Netlify, or Vercel
5. **Configure domain** - Point mockbizops.com to your hosting
6. **Add content** - Create more guides and examples
7. **Setup analytics** - Track usage

## Support

Need help?
- Check the main project `README.md`
- See `DEPLOYMENT.md` for backend deployment
- Review `FRONTEND_INTEGRATION.md` for integration guides

---

**You now have a complete, professional API documentation website!** 🎉
