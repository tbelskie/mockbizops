# Project Context & Architectural Decisions

This document captures the key decisions, context, and architectural choices made during the development of Mock BizOps.

## Project Overview

**Mock BizOps** is a production-quality mock API platform for business operations data, starting with a Car Repair Shop API. The goal is to provide developers with realistic mock data for testing, learning, and building prototypes.

### Vision

Create a platform similar to JSONPlaceholder or ReqRes, but for business operations:
- Car repair shops (current)
- Restaurants (future)
- E-commerce (future)
- Healthcare (future)
- etc.

## Two-Part Architecture

The project consists of **TWO separate deployable components**:

### 1. API Backend (`app/` folder)
- **Purpose**: The actual API that returns data
- **Technology**: FastAPI (Python 3.11+), PostgreSQL, SQLAlchemy
- **Deploy to**: Railway (recommended) or Render
- **URL**: `https://your-app.up.railway.app`
- **What it does**:
  - Serves REST API endpoints
  - Authenticates with API keys
  - Returns mock business data
  - Provides auto-generated Swagger docs at `/docs`

### 2. Documentation Website (`docs-site/` folder)
- **Purpose**: Developer portal that teaches how to use the API
- **Technology**: Pure HTML/CSS/JavaScript (no frameworks)
- **Deploy to**: GitHub Pages, Netlify, or Vercel
- **URL**: `mockbizops.com` (or similar)
- **What it does**:
  - Landing/marketing page
  - Getting started guide
  - Code examples (cURL, JavaScript, Python)
  - Interactive API playground
  - Complete API reference

**Key Point**: These are SEPARATE deployments. The docs site is NOT a data dashboard - it's an API documentation portal like stripe.com/docs or twilio.com/docs.

## Critical Architectural Decision: Shared Dataset Model

### Decision: Use Shared Dataset (Not Per-Developer Datasets)

**Date Decided**: During initial development
**Status**: ✅ Implemented

### The Question

Should each developer get their own isolated dataset, or should all developers share the same mock data?

### Decision: Shared Dataset

**All developers share the same pre-seeded mock data.**

### Rationale

1. **Industry Standard**: This is how successful mock APIs work
   - JSONPlaceholder - shared posts/users
   - ReqRes - shared user data
   - Dog API - shared images
   - Random User Generator - shared pool

2. **Cost-Effective**:
   - One Railway instance: $5-20/month
   - One PostgreSQL database
   - Supports unlimited developers
   - Free tier viable

3. **Developer Experience**:
   - ✅ Instant access - no setup required
   - ✅ No deployment needed
   - ✅ Just get API key and start using
   - ✅ Predictable, documentable data

4. **Documentation-Friendly**:
   - Can provide specific IDs in examples
   - "Try this customer: `550e8400-...`" works for everyone
   - Easier to write tutorials
   - Consistent across all docs

5. **Current Implementation**:
   - Code is already designed for this
   - Single database architecture
   - API key pool accessing same data
   - Works perfectly for mock/test use cases

### Rejected Alternative: Per-Developer Datasets

**Why not give each developer their own database?**

❌ **Cost**: $5-20/month × N developers = expensive
❌ **Complexity**: Would need multi-tenant architecture
❌ **Developer friction**: Would require setup/deployment
❌ **Unnecessary**: Developers don't need isolated data for testing
❌ **Not standard**: Mock APIs typically use shared data

### Future Consideration

Could offer BOTH models as tiered pricing:

**Free Tier**:
- Shared dataset
- 10,000 requests/month
- Standard API access

**Pro Tier** ($29/month):
- Optional private dataset
- Ability to reseed
- Custom data generation
- Higher rate limits

But **start with shared** for simplicity and standard practice.

## Data Generation Strategy

### How It Works

**Data is NOT pre-existing** - it's generated programmatically using Faker library.

**Process**:
1. Deploy API to Railway
2. Run seed script **ONCE**: `railway run python -m app.seed_data`
3. Data is saved to PostgreSQL
4. Data persists and is stable
5. All developers query the same data

### What Gets Generated

**File**: `app/seed_data.py`

**Generated data**:
- 500 customers (faker names, emails, addresses)
- 750 vehicles (real car makes/models)
- 50 mechanics (certifications, specialties, hourly rates)
- 2,000 work orders (with proper business logic)
- ~5,000 parts (from predefined realistic catalog)
- ~3,000 labor items (from predefined task list)
- 2 test API keys

**Key characteristics**:
- ✅ Uses Faker library for realistic names, addresses, etc.
- ✅ Predefined catalogs for parts and labor tasks
- ✅ Business logic (tax calculations, payment status, etc.)
- ✅ Distributed over 2 years of dates
- ✅ Proper relationships between entities
- ✅ Realistic pricing and hourly rates

### Data Stability

**Critical**: Once seeded, data is **stable and persistent**:
- Same customer IDs work every time
- Same work orders returned on each query
- Developers can rely on specific IDs
- Acts like a real production database
- Only changes if you explicitly re-seed

### Developer Workflow

**Developers DO NOT run seed script themselves.**

1. Developer visits mockbizops.com
2. Gets API key (or uses test key)
3. Makes API calls immediately
4. Sees the pre-seeded data you created
5. Can explore and pick specific IDs to use
6. Build their app against stable, predictable data

Example:
```javascript
// Developer explores once
const customers = await api.getCustomers();
console.log(customers.items[0].id);
// "550e8400-e29b-41d4-a716-446655440000"

// Then uses that ID throughout their app
const customer = await api.getCustomer("550e8400-...");
// Always returns same customer - stable!
```

## Technology Choices

### Backend

**FastAPI (Python 3.11+)**
- Modern, fast, auto-generates OpenAPI docs
- Easy to understand and modify
- Great for REST APIs
- Excellent documentation

**PostgreSQL + SQLAlchemy**
- Industry standard relational database
- Perfect for structured business data
- Easy to host (Railway, Supabase, etc.)
- SQLAlchemy ORM makes queries simple

**API Key Authentication**
- Simple `X-API-Key` header
- Stored in database
- Easy for developers to understand
- No OAuth complexity needed for mock API

### Documentation Site

**Pure HTML/CSS/JavaScript**
- No build step required
- No framework lock-in
- Fast loading
- Easy to customize
- Works on any static host
- Stripe-inspired design

**Why no framework?**
- Not needed for documentation
- Simpler to maintain
- Easier for others to contribute
- No build complexity
- Deploys anywhere instantly

## Deployment Strategy

### API Backend (Railway - Recommended)

**Why Railway?**
- ✅ All-in-one (app + database)
- ✅ Automatic GitHub deployments
- ✅ Easy environment variable management
- ✅ PostgreSQL included
- ✅ Free tier available
- ✅ Simple CLI: `railway run python -m seed_data`

**Process**:
1. Push to GitHub
2. Connect Railway to repo
3. Add PostgreSQL service
4. Set environment variables
5. Deploy (automatic)
6. Seed database (once)

**Alternative: Render**
- Similar features
- Slightly different pricing
- Good alternative if Railway has issues

### Documentation Site (GitHub Pages - Recommended)

**Why GitHub Pages?**
- ✅ 100% free
- ✅ Custom domain support
- ✅ Automatic deploys from git push
- ✅ Fast CDN
- ✅ Perfect for static sites
- ✅ Dead simple setup

**Process**:
1. Create separate repo for docs-site/
2. Push to GitHub
3. Enable Pages in repo settings
4. Add custom domain
5. Configure DNS

**Alternatives**:
- **Netlify**: Also free, drag-and-drop deploy, great UX
- **Vercel**: Also free, fast, great for SPAs
- **Cloudflare Pages**: Also free, fastest CDN

### Why Separate Repos?

**Could** keep everything in one repo, but **recommend separate repos**:

**Pros of separation**:
- ✅ Cleaner deployments
- ✅ Different CI/CD pipelines
- ✅ Different deployment cadences
- ✅ Can update docs without touching API
- ✅ Clearer responsibility boundaries

**Current setup**:
- One repo has everything (for initial push)
- Can split later if desired
- Or deploy from subdirectories

## API Design Decisions

### Pagination

**Default**: 20 items per page
**Max**: 100 items per page
**Format**: Limit/offset style

**Response includes metadata**:
```json
{
  "items": [...],
  "total": 500,
  "page": 1,
  "page_size": 20,
  "total_pages": 25
}
```

### Filtering

All list endpoints support filtering:
- Work orders: by status, priority, payment_status, date range
- Customers: by state, search (name/email/phone)
- Vehicles: by make, model, year
- Mechanics: by certification, specialty, active status

### Sorting

Standard `sort_by` and `order` parameters:
```
GET /work-orders?sort_by=total_amount&order=desc
```

### Error Handling

Standard HTTP status codes:
- 200: Success
- 400: Bad request
- 401: Unauthorized (missing/invalid API key)
- 404: Not found
- 429: Rate limited
- 500: Server error

JSON error format:
```json
{
  "detail": "Error message here"
}
```

### CORS

**Important**: Must configure CORS_ORIGINS environment variable:
```
CORS_ORIGINS=https://mockbizops.com,https://www.mockbizops.com
```

This allows docs site to call API from browser.

## Authentication Model

### API Keys

**Format**: UUID strings (e.g., `550e8400-e29b-41d4-a716-446655440000`)

**Storage**: PostgreSQL table with:
- key (unique)
- name (description)
- is_active (boolean)
- created_at
- last_used_at

**Usage**: Include in `X-API-Key` header:
```bash
curl -H "X-API-Key: your-key-here" https://api.mockbizops.com/v1/customers
```

### Admin Key

**Separate admin key** for admin operations:
- Generate new API keys
- List all keys
- Revoke keys

Set via `ADMIN_API_KEY` environment variable.

### Test Keys

After seeding, two test keys are created:
- `test-key-1234567890`
- `demo-key-abcdefghij`

**Public test keys are fine** for a mock API - this is expected behavior.

## Business Logic & Data Relationships

### Realistic Business Rules

The seed script implements real business logic:

1. **Work Order Status**:
   - Older orders (>14 days) → 95% completed, 5% cancelled
   - Medium age (7-14 days) → 70% completed, 20% in-progress, 10% waiting parts
   - Recent (<7 days) → 30% pending, 50% in-progress, 20% completed

2. **Pricing**:
   - Parts cost from predefined catalog
   - Labor = hours × mechanic hourly rate
   - Tax = 8% on (parts + labor)
   - Total = parts + labor + tax

3. **Payment**:
   - Completed orders: 85% paid, 10% unpaid, 5% partial
   - Non-completed orders: 100% unpaid

4. **Mechanic Rates**:
   - Apprentice: $25-40/hr
   - Journeyman: $40-65/hr
   - Master: $65-95/hr

5. **Vehicle Mileage**:
   - Based on age: age × 8,000-15,000 miles + random 0-10,000

6. **Work Order Numbers**:
   - Format: `WO-YYYYMMDD-XXXX`
   - Sequential per day
   - Example: `WO-20241112-0001`

### Data Relationships

```
Customer
  ├─→ Vehicles (1:many)
  └─→ Work Orders (1:many)

Vehicle
  ├─→ Customer (many:1)
  └─→ Work Orders (1:many)

Work Order
  ├─→ Customer (many:1)
  ├─→ Vehicle (many:1)
  ├─→ Mechanic (many:1)
  ├─→ Parts (1:many)
  └─→ Labor Items (1:many)

Mechanic
  ├─→ Work Orders (1:many)
  └─→ Labor Items (1:many)
```

## Documentation Philosophy

### Target Audience

**Primary**: Frontend developers who need mock data
**Secondary**: Backend developers learning API integration
**Tertiary**: Students and educators

### Documentation Structure

**Landing Page** (`index.html`):
- Quick value proposition
- Key features
- Use cases
- Pricing
- Call to action

**Getting Started** (`docs.html`):
- Authentication guide
- First API call
- Code examples in multiple languages
- Pagination, filtering, errors
- Best practices

**API Reference** (`api-reference.html`):
- Complete endpoint documentation
- Request/response examples
- All parameters documented
- Status codes

**Interactive Playground** (`playground.html`):
- Test API in browser
- No coding required
- See real responses
- Generate API keys

### Code Examples

**Always provide examples in**:
- cURL (universal)
- JavaScript (most common for frontend)
- Python (popular for backend/scripting)

**Keep examples simple and copy-pasteable.**

## Future Enhancements

### Phase 1 (Current) ✅
- [x] Car Repair Shop API
- [x] Documentation site
- [x] Deployment guides
- [x] Seed script
- [x] API key authentication

### Phase 2 (Near Future)
- [ ] Add more business datasets (restaurant, e-commerce, etc.)
- [ ] API key dashboard (manage keys via web UI)
- [ ] Usage analytics (show request counts)
- [ ] Rate limiting implementation
- [ ] SDK packages (npm, PyPI)

### Phase 3 (Later)
- [ ] Pro tier with private datasets
- [ ] Custom data generation
- [ ] Webhook simulation
- [ ] GraphQL endpoint
- [ ] OpenAPI spec download

### Phase 4 (Advanced)
- [ ] Multi-tenant architecture
- [ ] Per-developer data isolation (if needed)
- [ ] Custom business logic injection
- [ ] Data versioning (v1, v2 datasets)

## Important Files Reference

### Core Backend Files
- `app/main.py` - FastAPI entry point
- `app/models/*.py` - Database schemas (7 models)
- `app/routers/*.py` - API endpoints (6 routers)
- `app/seed_data.py` - Data generation script
- `app/auth.py` - API key authentication
- `app/config.py` - Configuration management

### Documentation Site Files
- `docs-site/index.html` - Landing page
- `docs-site/docs.html` - Getting started guide
- `docs-site/playground.html` - Interactive tester
- `docs-site/css/style.css` - Stripe-inspired styling
- `docs-site/js/main.js` - Interactivity

### Deployment & Configuration
- `Dockerfile` - Container configuration
- `docker-compose.yml` - Local development
- `railway.toml` - Railway deployment config
- `render.yaml` - Render deployment config
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variable template

### Documentation
- `README.md` - Main project documentation
- `START_HERE.md` - Quick overview
- `QUICKSTART.md` - 5-minute API deployment
- `DEPLOYMENT.md` - Detailed deployment options
- `DOCS_SITE_DEPLOYMENT.md` - Deploy docs site
- `PROJECT_SUMMARY.md` - Complete project summary
- `ARCHITECTURE.md` - System architecture
- `FRONTEND_INTEGRATION.md` - How to integrate
- `CLAUDE.md` - This file (context & decisions)

## Environment Variables

### Required (API Backend)

```env
# Database
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Security
SECRET_KEY=<random-string-32-chars>
ADMIN_API_KEY=<uuid-or-random-string>

# CORS (Important!)
CORS_ORIGINS=https://mockbizops.com,https://www.mockbizops.com
```

### Optional

```env
ENVIRONMENT=production
DEBUG=false
DEFAULT_PAGE_SIZE=20
MAX_PAGE_SIZE=100
```

### Generate Secure Keys

```bash
# SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# ADMIN_API_KEY
python -c "import uuid; print(str(uuid.uuid4()))"
```

## Common Gotchas & Solutions

### 1. CORS Errors in Playground

**Problem**: Playground can't call API from browser

**Solution**: Add docs site domain to CORS_ORIGINS:
```env
CORS_ORIGINS=https://mockbizops.com,http://localhost:8080
```

### 2. API Returns Empty Data

**Problem**: Database not seeded

**Solution**: Run seed script:
```bash
railway run python -m app.seed_data
```

### 3. Docs Site Shows Wrong API URL

**Problem**: Placeholder URLs in playground/docs

**Solution**: Update in these files:
- `docs-site/playground.html` - Line ~95
- `docs-site/docs.html` - All code examples
- Replace `https://api.mockbizops.com` with your Railway URL

### 4. Can't Generate New API Keys

**Problem**: Not using admin key

**Solution**: Use ADMIN_API_KEY value in X-API-Key header for admin endpoints

## Testing Checklist

### Before Going Live

**API Backend**:
- [ ] Deploy to Railway
- [ ] PostgreSQL connected
- [ ] Environment variables set
- [ ] Seed database
- [ ] Test: `curl https://your-app.railway.app/health`
- [ ] Test: Get customers with test API key
- [ ] Check Swagger docs at `/docs`

**Documentation Site**:
- [ ] Deploy to GitHub Pages/Netlify
- [ ] Update all API URLs
- [ ] Test landing page loads
- [ ] Test docs page loads
- [ ] Test playground connects to API
- [ ] Test code examples work
- [ ] Test on mobile

**Integration**:
- [ ] CORS configured correctly
- [ ] Playground can call API
- [ ] API keys work
- [ ] Test all endpoints return data
- [ ] Error handling works

## Cost Breakdown

### Free Tier (Development)

- Railway: $5 credit/month (~500 hours)
- GitHub Pages: FREE
- Domain: Not needed (use Railway/GitHub URLs)

**Total**: FREE for testing

### Production

- Railway: ~$5-20/month (depends on usage)
- GitHub Pages: FREE
- Domain: ~$12/year (optional)

**Total**: ~$5-20/month + $12/year domain

### Scalability

Can support thousands of developers on single Railway instance:
- Database queries are simple
- Data is read-only
- No heavy computation
- Can upgrade Railway plan if needed

## Support & Maintenance

### Regular Tasks

**Weekly**:
- Monitor Railway usage/costs
- Check error logs

**Monthly**:
- Review API usage patterns
- Update documentation if needed
- Check for security updates

**Quarterly**:
- Consider re-seeding data (if desired)
- Review and update pricing
- Add new features

### Community

Consider adding:
- GitHub Discussions
- Discord server
- Twitter for updates
- Newsletter for developers

## Key Design Principles

1. **Simplicity First**: Keep it simple - no over-engineering
2. **Developer Experience**: Make it dead simple to start using
3. **Realistic Data**: Business logic should make sense
4. **Stable & Predictable**: Data shouldn't change unexpectedly
5. **Well Documented**: Clear examples, multiple languages
6. **Free Tier Friendly**: Keep costs low, enable wide adoption
7. **Standards Based**: REST, OpenAPI, standard HTTP

## Success Metrics

### Goals

**Phase 1** (First 3 months):
- 100+ developers signed up
- 10,000+ API requests
- Documentation site visits

**Phase 2** (6 months):
- 1,000+ developers
- 100,000+ API requests
- Featured in developer newsletters/blogs

**Phase 3** (12 months):
- 5,000+ developers
- Multiple business datasets
- Sustainable revenue (if monetizing)

### Analytics to Track

- API requests per day/month
- Unique API keys used
- Documentation site visits
- Popular endpoints
- Error rates
- Response times

## Contact & Contribution

**Repository**: https://github.com/tbelskie/mockbizops

**Issues**: Use GitHub issues for bug reports

**Contributions**: Pull requests welcome

**Future Datasets**: Open to suggestions for new business types

---

## Summary

**Mock BizOps** is a shared-dataset mock API platform designed to help developers build and test applications without setting up their own backend.

**Key points**:
- ✅ Shared data model (all developers see same data)
- ✅ Two-part system (API backend + docs site)
- ✅ Deploy once, use forever
- ✅ Simple, cost-effective, developer-friendly
- ✅ Production-quality realistic data
- ✅ Well-documented with examples

**This document should be updated as the project evolves and new decisions are made.**

Last Updated: 2024-11-12
