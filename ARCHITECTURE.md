# Architecture Overview

## How Your Custom Website Connects to Railway Backend

```
┌─────────────────────────────────────────────────────────────────┐
│                     YOUR CUSTOM WEBSITE                          │
│                  (Hosted Anywhere You Want)                      │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ GitHub Pages │  │   Vercel     │  │   Netlify    │ ... etc │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                  │
│         Your HTML/React/Vue/Next.js Frontend                    │
│              with your own design                               │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         │ HTTP Requests
                         │ (with X-API-Key header)
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  RAILWAY (Backend API)                           │
│              https://your-app.up.railway.app                     │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  FastAPI Application (Python)                             │ │
│  │  ┌─────────────────────────────────────────────────────┐ │ │
│  │  │ API Endpoints:                                      │ │ │
│  │  │  • GET /api/v1/customers                           │ │ │
│  │  │  • GET /api/v1/vehicles                            │ │ │
│  │  │  • GET /api/v1/work-orders                         │ │ │
│  │  │  • GET /api/v1/work-orders/stats                   │ │ │
│  │  │  • ... and more                                    │ │ │
│  │  └─────────────────────────────────────────────────────┘ │ │
│  └───────────────────────┬───────────────────────────────────┘ │
│                          │                                      │
│                          ▼                                      │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  PostgreSQL Database                                      │ │
│  │  • 500 customers                                          │ │
│  │  • 750 vehicles                                           │ │
│  │  • 2,000+ work orders                                     │ │
│  │  • Parts, labor, mechanics                                │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Example

### 1. User visits your website
```
User → https://yourdomain.com
```

### 2. Website loads and fetches data
```javascript
// Your website's JavaScript
fetch('https://your-app.up.railway.app/api/v1/customers', {
    headers: {
        'X-API-Key': 'test-key-1234567890'
    }
})
```

### 3. Railway API processes request
```
Railway API → Authenticates API key
           → Queries PostgreSQL database
           → Returns JSON data
```

### 4. Your website displays data
```javascript
// Your website receives:
{
    "items": [
        {
            "id": "...",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            ...
        }
    ],
    "total": 500,
    "page": 1
}

// Display in your custom UI
```

## Component Breakdown

### Your Website (Frontend)
**You control:**
- ✅ All design and styling
- ✅ User interface
- ✅ User experience
- ✅ Navigation and layout
- ✅ Branding and colors
- ✅ Custom features

**Location options:**
- GitHub Pages (free)
- Vercel (free)
- Netlify (free)
- Your own hosting
- Cloudflare Pages (free)

### Railway Backend (API)
**Provides:**
- ✅ RESTful API endpoints
- ✅ Data storage (PostgreSQL)
- ✅ Authentication (API keys)
- ✅ Business logic
- ✅ Data validation
- ✅ Automatic documentation

**Railway handles:**
- Server management
- Database hosting
- Automatic deployments
- HTTPS/SSL
- Monitoring

## Example: Building a Dashboard

### Step 1: Design Your Website
```html
<!-- Your custom design -->
<div class="my-dashboard">
    <header class="my-header">
        <img src="my-logo.png">
        <h1>My Car Repair Business</h1>
    </header>

    <div id="statistics">
        <!-- Your custom stats display -->
    </div>

    <div id="customers">
        <!-- Your custom customer list -->
    </div>
</div>
```

### Step 2: Connect to Railway API
```javascript
// Fetch data from Railway
async function loadStats() {
    const response = await fetch(
        'https://your-app.up.railway.app/api/v1/work-orders/stats',
        {
            headers: { 'X-API-Key': 'your-key' }
        }
    );
    const stats = await response.json();

    // Display in your custom UI
    document.getElementById('statistics').innerHTML = `
        <div class="stat-card">
            <h2>$${stats.total_revenue}</h2>
            <p>Total Revenue</p>
        </div>
    `;
}
```

### Step 3: Deploy Anywhere
```bash
# Option 1: GitHub Pages
git push to GitHub → Enable Pages → Done

# Option 2: Netlify
netlify deploy → Done

# Option 3: Vercel
vercel → Done
```

## Available API Endpoints

### Customer Endpoints
- `GET /api/v1/customers` - List all customers
- `GET /api/v1/customers/{id}` - Get customer details
- `GET /api/v1/customers/{id}/vehicles` - Customer's vehicles
- `GET /api/v1/customers/{id}/work-orders` - Customer's orders

### Vehicle Endpoints
- `GET /api/v1/vehicles` - List all vehicles
- `GET /api/v1/vehicles/{id}` - Get vehicle details
- `GET /api/v1/vehicles/{id}/work-orders` - Vehicle history

### Work Order Endpoints
- `GET /api/v1/work-orders` - List all work orders
- `GET /api/v1/work-orders/{id}` - Get order details
- `GET /api/v1/work-orders/stats` - Statistics

### Parts & Mechanics
- `GET /api/v1/parts` - List parts
- `GET /api/v1/mechanics` - List mechanics
- `GET /api/v1/mechanics/{id}/work-orders` - Mechanic's orders

## Real-World Example Architectures

### Architecture 1: Simple Static Site
```
GitHub Pages (Frontend)
    ↓ API calls
Railway (Backend + DB)
```

**Best for:**
- Simple dashboards
- Public data display
- Quick prototypes

### Architecture 2: React Application
```
Vercel (React App)
    ↓ API calls
Railway (Backend + DB)
```

**Best for:**
- Complex UIs
- Single-page apps
- Modern web apps

### Architecture 3: Multi-site
```
Website 1 (Public site) ─┐
Website 2 (Admin panel) ─┼─→ Railway (Backend + DB)
Mobile App             ──┘
```

**Best for:**
- Multiple interfaces
- Different user types
- Mobile + web

### Architecture 4: Secure Architecture
```
Your Website
    ↓
Your Serverless Functions (API Key hidden)
    ↓
Railway (Backend + DB)
```

**Best for:**
- Sensitive operations
- Hidden API keys
- Production apps

## Security Considerations

### ✅ Safe to Expose
- API endpoint URL
- Public API keys (limited permissions)
- Health check endpoint

### ⚠️ Keep Secret
- Admin API key
- Database credentials
- Railway dashboard access

### 🔒 Best Practices
1. Use separate API keys for frontend
2. Enable CORS only for your domains
3. Implement rate limiting
4. Monitor API usage
5. Rotate keys regularly

## CORS Configuration

Railway environment variable:
```
# Allow your domains
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Development
CORS_ORIGINS=http://localhost:3000,http://localhost:8080

# Both
CORS_ORIGINS=https://yourdomain.com,http://localhost:3000
```

## Testing Your Setup

### 1. Test Railway API
```bash
curl https://your-app.up.railway.app/health
# Should return: {"status": "healthy"}
```

### 2. Test Authentication
```bash
curl -H "X-API-Key: test-key-1234567890" \
    https://your-app.up.railway.app/api/v1/customers
# Should return customer data
```

### 3. Test from Browser Console
```javascript
fetch('https://your-app.up.railway.app/api/v1/work-orders/stats', {
    headers: { 'X-API-Key': 'test-key-1234567890' }
})
.then(r => r.json())
.then(data => console.log(data));
```

## Common Issues

### CORS Error
```
Access to fetch has been blocked by CORS policy
```
**Solution:** Add your domain to `CORS_ORIGINS` in Railway

### 401 Unauthorized
```
Missing API key or invalid
```
**Solution:** Include `X-API-Key` header in all requests

### API Not Responding
**Check:**
- Railway service is running
- Database is connected
- Environment variables are set

## Summary

✅ **YES** - You can use Railway as your backend
✅ **YES** - You can host your website anywhere
✅ **YES** - You have full control over your website design
✅ **YES** - Multiple websites can use the same API
✅ **YES** - You can use any frontend framework

**Railway = Backend & Database**
**Your Website = Frontend & Design**

They communicate via simple HTTP requests!
