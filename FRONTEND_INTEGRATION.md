# Frontend Integration Guide

Connect your custom website to the Railway-hosted API backend.

## Overview

Your setup will be:
- **Backend API**: Hosted on Railway (e.g., `https://car-repair-api.up.railway.app`)
- **Frontend Website**: Hosted anywhere (Vercel, Netlify, GitHub Pages, your own server, etc.)
- **Communication**: Frontend makes HTTP requests to Railway API

## Step 1: Configure CORS

Update your Railway environment variables to allow requests from your website:

### In Railway Dashboard:

Add or update the `CORS_ORIGINS` variable:

```
# Single domain
CORS_ORIGINS=https://yourdomain.com

# Multiple domains (comma-separated)
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com,http://localhost:3000

# Allow all domains (for development only, not recommended for production)
CORS_ORIGINS=*
```

**Important**: Include all domains where your frontend will be hosted, including:
- Your production domain (`https://yourdomain.com`)
- Your www subdomain (`https://www.yourdomain.com`)
- Local development (`http://localhost:3000`, `http://127.0.0.1:3000`)

## Step 2: Get Your API URL

After deploying to Railway, your API URL will be:

```
https://your-app-name.up.railway.app
```

You can find it in:
- Railway Dashboard → Your Service → Settings → Domains

## Step 3: Choose Your Frontend Approach

### Option A: Vanilla HTML/JavaScript (Simplest)

Create a simple website that calls your API:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Car Repair Shop Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .customer-card {
            border: 1px solid #ddd;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
        }
        .loading { color: #666; }
        .error { color: red; }
    </style>
</head>
<body>
    <h1>Car Repair Shop - Customer List</h1>
    <div id="customers"></div>

    <script>
        // Configuration
        const API_URL = 'https://your-app.up.railway.app/api/v1';
        const API_KEY = 'test-key-1234567890';

        // Fetch customers
        async function loadCustomers() {
            const container = document.getElementById('customers');
            container.innerHTML = '<p class="loading">Loading customers...</p>';

            try {
                const response = await fetch(`${API_URL}/customers?page=1&page_size=10`, {
                    headers: {
                        'X-API-Key': API_KEY
                    }
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();

                // Display customers
                container.innerHTML = '';
                data.items.forEach(customer => {
                    const card = document.createElement('div');
                    card.className = 'customer-card';
                    card.innerHTML = `
                        <h3>${customer.first_name} ${customer.last_name}</h3>
                        <p>Email: ${customer.email}</p>
                        <p>Phone: ${customer.phone}</p>
                        <p>Location: ${customer.city}, ${customer.state}</p>
                        <p>Customer since: ${new Date(customer.customer_since).toLocaleDateString()}</p>
                    `;
                    container.appendChild(card);
                });

                // Add pagination info
                const pagination = document.createElement('p');
                pagination.textContent = `Showing ${data.items.length} of ${data.total} customers`;
                container.appendChild(pagination);

            } catch (error) {
                container.innerHTML = `<p class="error">Error loading customers: ${error.message}</p>`;
                console.error('Error:', error);
            }
        }

        // Load on page load
        loadCustomers();
    </script>
</body>
</html>
```

**Deploy this to**:
- GitHub Pages (free)
- Netlify (free)
- Vercel (free)
- Your own web hosting

### Option B: React Application

```bash
# Create React app
npx create-react-app car-repair-dashboard
cd car-repair-dashboard
npm install axios
```

**src/config.js**:
```javascript
export const API_URL = 'https://your-app.up.railway.app/api/v1';
export const API_KEY = 'test-key-1234567890';
```

**src/services/api.js**:
```javascript
import axios from 'axios';
import { API_URL, API_KEY } from '../config';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'X-API-Key': API_KEY
    }
});

export const getCustomers = async (page = 1, pageSize = 20) => {
    const response = await api.get('/customers', {
        params: { page, page_size: pageSize }
    });
    return response.data;
};

export const getCustomer = async (id) => {
    const response = await api.get(`/customers/${id}`);
    return response.data;
};

export const getWorkOrders = async (filters = {}) => {
    const response = await api.get('/work-orders', { params: filters });
    return response.data;
};

export const getWorkOrderStats = async () => {
    const response = await api.get('/work-orders/stats');
    return response.data;
};

export default api;
```

**src/App.js**:
```javascript
import React, { useState, useEffect } from 'react';
import { getCustomers, getWorkOrderStats } from './services/api';
import './App.css';

function App() {
    const [customers, setCustomers] = useState([]);
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            const [customersData, statsData] = await Promise.all([
                getCustomers(1, 10),
                getWorkOrderStats()
            ]);
            setCustomers(customersData.items);
            setStats(statsData);
        } catch (error) {
            console.error('Error loading data:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) return <div>Loading...</div>;

    return (
        <div className="App">
            <header>
                <h1>Car Repair Shop Dashboard</h1>
            </header>

            {stats && (
                <section className="stats">
                    <h2>Statistics</h2>
                    <div className="stat-cards">
                        <div className="stat-card">
                            <h3>Total Orders</h3>
                            <p>{stats.total_orders}</p>
                        </div>
                        <div className="stat-card">
                            <h3>Total Revenue</h3>
                            <p>${stats.total_revenue}</p>
                        </div>
                        <div className="stat-card">
                            <h3>Pending Orders</h3>
                            <p>{stats.pending_orders}</p>
                        </div>
                    </div>
                </section>
            )}

            <section className="customers">
                <h2>Recent Customers</h2>
                <div className="customer-list">
                    {customers.map(customer => (
                        <div key={customer.id} className="customer-card">
                            <h3>{customer.first_name} {customer.last_name}</h3>
                            <p>{customer.email}</p>
                            <p>{customer.city}, {customer.state}</p>
                        </div>
                    ))}
                </div>
            </section>
        </div>
    );
}

export default App;
```

**Deploy to**:
- Vercel: `npm run build && vercel`
- Netlify: Drag & drop build folder
- GitHub Pages: `npm run build && gh-pages -d build`

### Option C: Next.js (React with SSR)

```bash
npx create-next-app@latest car-repair-dashboard
cd car-repair-dashboard
npm install axios
```

Similar structure to React, but with server-side rendering capabilities.

### Option D: Vue.js

```bash
npm create vue@latest car-repair-dashboard
cd car-repair-dashboard
npm install axios
```

Similar API integration patterns to React.

## Step 4: Environment Variables (Best Practice)

Instead of hardcoding API credentials, use environment variables:

### For React/Next.js:

Create `.env.local`:
```
REACT_APP_API_URL=https://your-app.up.railway.app/api/v1
REACT_APP_API_KEY=test-key-1234567890
```

Or for Next.js:
```
NEXT_PUBLIC_API_URL=https://your-app.up.railway.app/api/v1
NEXT_PUBLIC_API_KEY=test-key-1234567890
```

Use in code:
```javascript
const API_URL = process.env.REACT_APP_API_URL;
const API_KEY = process.env.REACT_APP_API_KEY;
```

### For Static HTML (using build tools):

Use a config file that gets replaced during deployment:

**config.template.js**:
```javascript
window.APP_CONFIG = {
    apiUrl: '${API_URL}',
    apiKey: '${API_KEY}'
};
```

## Step 5: Security Considerations

### ⚠️ API Key Exposure

**Important**: Since frontend code runs in the browser, your API key will be visible to users.

**Solutions**:

1. **Generate Public API Keys** (Recommended)
   - Create API keys specifically for frontend use
   - Limit permissions if possible
   - Rotate keys regularly

2. **Add Backend Middleware** (Advanced)
   - Create a thin backend layer (serverless function)
   - Frontend calls your serverless function
   - Serverless function calls Railway API with secret key

3. **Rate Limiting** (Important)
   - Implement rate limiting on your Railway API
   - Prevents abuse even if key is exposed

### Example: Using Vercel Serverless Functions

**api/customers.js**:
```javascript
// This runs on Vercel's server, not in browser
export default async function handler(req, res) {
    const API_KEY = process.env.API_KEY; // Secret, not exposed

    const response = await fetch(
        'https://your-app.up.railway.app/api/v1/customers',
        {
            headers: { 'X-API-Key': API_KEY }
        }
    );

    const data = await response.json();
    res.status(200).json(data);
}
```

Frontend calls `/api/customers` instead of Railway directly.

## Step 6: Example Projects

### Dashboard Example

Create a full dashboard with:
- Customer list and search
- Work order management
- Statistics and charts
- Vehicle service history

### Public API Portal

Create a developer portal:
- API documentation
- API key signup
- Usage statistics
- Code examples

### Mobile App

Use React Native or Flutter:
- Same API calls
- Mobile-friendly UI
- Push notifications for order updates

## Frontend Hosting Options

| Platform | Best For | Free Tier | Deploy |
|----------|----------|-----------|--------|
| **Vercel** | React/Next.js | Yes | `vercel` |
| **Netlify** | Any static site | Yes | Drag & drop |
| **GitHub Pages** | Simple sites | Yes | Push to repo |
| **Cloudflare Pages** | Static sites | Yes | Git integration |
| **AWS S3 + CloudFront** | Large scale | Generous | AWS CLI |

## Complete Example Repository

I can create a complete frontend example if you want. What framework do you prefer?

- [ ] Vanilla HTML/JS (simplest)
- [ ] React (most popular)
- [ ] Next.js (React with SSR)
- [ ] Vue.js
- [ ] Svelte

## Testing Your Integration

1. **Test CORS**:
```javascript
fetch('https://your-app.up.railway.app/health')
    .then(r => r.json())
    .then(data => console.log('API is accessible:', data));
```

2. **Test Authentication**:
```javascript
fetch('https://your-app.up.railway.app/api/v1/customers', {
    headers: { 'X-API-Key': 'test-key-1234567890' }
})
.then(r => r.json())
.then(data => console.log('Customers:', data));
```

3. **Check Browser Console**:
- Look for CORS errors
- Check network tab for API calls
- Verify response data

## Example: Full Dashboard Components

Need help building specific components? I can create:

1. **Customer search and filter**
2. **Work order timeline**
3. **Statistics dashboard with charts**
4. **Vehicle service history**
5. **Mechanic schedule view**

Just let me know what you need!

## Summary

✅ Railway hosts your API backend
✅ Your website calls Railway API via HTTP
✅ Set CORS_ORIGINS to allow your domain
✅ Include X-API-Key header in requests
✅ Deploy frontend anywhere (Vercel, Netlify, etc.)

**You have complete control over your website's design and functionality!**
