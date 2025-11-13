# Mock BizOps - Car Repair Shop API

A production-quality mock API service with professional developer documentation.

## 📦 What's In This Project

This project contains **TWO things**:

### 1. API Backend (`app/` folder)
The actual API that returns car repair shop data. Deploy to **Railway**.
- FastAPI application
- PostgreSQL database
- 2,000+ work orders, 500+ customers, 750+ vehicles
- 25+ REST endpoints

### 2. Documentation Website (`docs-site/` folder)
A professional developer portal (like stripe.com/docs). Deploy to **mockbizops.com**.
- Landing page
- Getting started guide
- Interactive API playground
- Code examples

## 🎯 Quick Navigation

**Choose your path:**

| I want to... | Go to |
|--------------|-------|
| **Deploy the API backend** | [QUICKSTART.md](QUICKSTART.md) - 5 minutes |
| **Deploy the docs website** | [docs-site/README.md](docs-site/README.md) |
| **Understand the architecture** | [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) |
| **See deployment options** | [DEPLOYMENT.md](DEPLOYMENT.md) |
| **Learn about frontend integration** | [FRONTEND_INTEGRATION.md](FRONTEND_INTEGRATION.md) |

## Features

- 🚗 **Customers**: Complete customer management with contact information and history
- 🔧 **Vehicles**: Vehicle tracking with VIN, make, model, and service history
- 📋 **Work Orders**: Comprehensive repair order management with status tracking
- 👨‍🔧 **Mechanics**: Mechanic profiles with certifications and specialties
- 📦 **Parts**: Parts inventory with pricing and warranty information
- 💼 **Labor Items**: Labor tracking with hours and rates
- 🔑 **API Key Authentication**: Secure access control
- 📊 **Statistics**: Work order statistics and analytics
- 🔍 **Filtering & Search**: Advanced filtering and search capabilities
- 📄 **Pagination**: Efficient pagination for all list endpoints

## Tech Stack

- **Backend**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: API key-based
- **Data Generation**: Faker library
- **Documentation**: Auto-generated OpenAPI/Swagger docs
- **Deployment**: Docker, Railway, Render

## 🚀 Deploy to Production

**Want to get this live on the internet?**

👉 **See [QUICKSTART.md](QUICKSTART.md)** for a 5-minute deployment guide

👉 **See [DEPLOYMENT.md](DEPLOYMENT.md)** for detailed deployment options

**Quick deploy:**
```bash
./setup_deployment.sh  # Generate keys
# Push to GitHub, deploy to Railway
# Full instructions in QUICKSTART.md
```

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- pip or poetry

### Local Development Setup

1. **Clone the repository**

```bash
cd mock_biz_ops
```

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

```bash
cp .env.example .env
# Edit .env with your database credentials
```

5. **Set up the database**

Create a PostgreSQL database:

```bash
createdb car_repair_api
```

6. **Seed the database**

```bash
python -m app.seed_data
```

This will generate:
- 500 customers
- 750 vehicles
- 50 mechanics
- 2,000 work orders with parts and labor
- Test API keys

7. **Run the development server**

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Using Docker

1. **Start with Docker Compose**

```bash
docker-compose up -d
```

This will start both PostgreSQL and the API server.

2. **Seed the database**

```bash
docker-compose exec api python -m app.seed_data
```

3. **View logs**

```bash
docker-compose logs -f api
```

## API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Authentication

All API endpoints require an API key. Include your API key in the `X-API-Key` header.

### Test API Keys

After seeding the database, you can use these test keys:

- `test-key-1234567890`
- `demo-key-abcdefghij`

### Example Request

```bash
curl -H "X-API-Key: test-key-1234567890" http://localhost:8000/api/v1/customers
```

## API Endpoints

### Customers

- `GET /api/v1/customers` - List all customers
  - Query params: `page`, `page_size`, `search`, `state`, `sort_by`, `order`
- `GET /api/v1/customers/{id}` - Get customer details
- `GET /api/v1/customers/{id}/vehicles` - Get customer's vehicles
- `GET /api/v1/customers/{id}/work-orders` - Get customer's work orders

### Vehicles

- `GET /api/v1/vehicles` - List all vehicles
  - Query params: `page`, `page_size`, `make`, `model`, `year`, `sort_by`, `order`
- `GET /api/v1/vehicles/{id}` - Get vehicle details
- `GET /api/v1/vehicles/{id}/work-orders` - Get vehicle service history

### Work Orders

- `GET /api/v1/work-orders` - List all work orders
  - Query params: `page`, `page_size`, `status`, `priority`, `payment_status`, `start_date`, `end_date`, `sort_by`, `order`
- `GET /api/v1/work-orders/{id}` - Get work order details
- `GET /api/v1/work-orders/{id}/parts` - Get parts for work order
- `GET /api/v1/work-orders/{id}/labor` - Get labor items for work order
- `GET /api/v1/work-orders/stats` - Get summary statistics

### Parts

- `GET /api/v1/parts` - List all parts
  - Query params: `page`, `page_size`, `work_order_id`, `part_number`, `supplier`, `sort_by`, `order`

### Mechanics

- `GET /api/v1/mechanics` - List all mechanics
  - Query params: `page`, `page_size`, `is_active`, `certification_level`, `specialty`, `sort_by`, `order`
- `GET /api/v1/mechanics/{id}` - Get mechanic details
- `GET /api/v1/mechanics/{id}/work-orders` - Get mechanic's assigned work orders

### Admin (API Key Management)

- `POST /api/v1/admin/api-keys` - Generate new API key (requires admin key)
- `GET /api/v1/admin/api-keys` - List all API keys (requires admin key)
- `DELETE /api/v1/admin/api-keys/{key}` - Revoke API key (requires admin key)

## Example Requests

### Using cURL

**List customers with search:**

```bash
curl -H "X-API-Key: test-key-1234567890" \
  "http://localhost:8000/api/v1/customers?search=john&page=1&page_size=10"
```

**Get work order details:**

```bash
curl -H "X-API-Key: test-key-1234567890" \
  "http://localhost:8000/api/v1/work-orders/{work_order_id}"
```

**Get work order statistics:**

```bash
curl -H "X-API-Key: test-key-1234567890" \
  "http://localhost:8000/api/v1/work-orders/stats"
```

### Using Python

```python
import requests

API_KEY = "test-key-1234567890"
BASE_URL = "http://localhost:8000/api/v1"

headers = {
    "X-API-Key": API_KEY
}

# List customers
response = requests.get(f"{BASE_URL}/customers", headers=headers)
customers = response.json()

# Get customer details
customer_id = customers["items"][0]["id"]
response = requests.get(f"{BASE_URL}/customers/{customer_id}", headers=headers)
customer = response.json()

# Get work order stats
response = requests.get(f"{BASE_URL}/work-orders/stats", headers=headers)
stats = response.json()
print(f"Total Revenue: ${stats['total_revenue']}")
```

### Using JavaScript

```javascript
const API_KEY = 'test-key-1234567890';
const BASE_URL = 'http://localhost:8000/api/v1';

const headers = {
  'X-API-Key': API_KEY
};

// List customers
fetch(`${BASE_URL}/customers`, { headers })
  .then(res => res.json())
  .then(data => console.log(data));

// Get work order details
const workOrderId = 1;
fetch(`${BASE_URL}/work-orders/${workOrderId}`, { headers })
  .then(res => res.json())
  .then(data => console.log(data));
```

## Database Schema

### Core Tables

**customers**
- Customer information (name, email, phone, address)
- Customer since date
- Notes

**vehicles**
- VIN, make, model, year, color
- License plate
- Current mileage
- Links to customer

**mechanics**
- Name and certification level
- Specialties (array)
- Hourly rate
- Active status

**work_orders**
- Work order number (auto-generated)
- Status (pending, in_progress, waiting_parts, completed, cancelled)
- Priority (low, normal, high, urgent)
- Description and diagnosis
- Odometer readings
- Financial calculations (parts, labor, tax, total)
- Payment status and method
- Links to customer, vehicle, and mechanic

**parts**
- Part number and description
- Quantity and pricing
- Supplier and warranty
- Links to work order

**labor_items**
- Description
- Hours and hourly rate
- Total cost
- Links to work order and mechanic

## Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/car_repair_api

# Security
SECRET_KEY=your-secret-key-here
ADMIN_API_KEY=admin-key-here

# Application
PROJECT_NAME=Car Repair Shop Mock API
VERSION=1.0.0
API_V1_PREFIX=/api/v1
ENVIRONMENT=development
DEBUG=true

# Pagination
DEFAULT_PAGE_SIZE=20
MAX_PAGE_SIZE=100

# CORS (comma-separated origins)
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

## Deployment

### Railway

1. Install Railway CLI: `npm install -g @railway/cli`
2. Login: `railway login`
3. Initialize: `railway init`
4. Add PostgreSQL: `railway add postgresql`
5. Deploy: `railway up`
6. Set environment variables in Railway dashboard
7. Seed database: `railway run python -m app.seed_data`

### Render

1. Create a new Web Service
2. Connect your repository
3. Use `render.yaml` for infrastructure as code
4. Set environment variables in Render dashboard
5. Deploy
6. Seed database using Render Shell

### Docker

Build and push to Docker Hub:

```bash
docker build -t yourusername/car-repair-api .
docker push yourusername/car-repair-api
```

## Development

### Project Structure

```
car-repair-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration
│   ├── database.py          # Database setup
│   ├── auth.py              # Authentication
│   ├── utils.py             # Utility functions
│   ├── seed_data.py         # Data generation
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   └── routers/             # API endpoints
├── tests/
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── Makefile
├── railway.toml
├── render.yaml
└── README.md
```

### Adding New Endpoints

1. Create route handler in appropriate router file
2. Define Pydantic schemas if needed
3. Add route to router
4. Test endpoint in Swagger UI

### Makefile Commands

```bash
make help          # Show available commands
make install       # Install dependencies
make dev           # Run development server
make seed          # Seed database
make docker-up     # Start Docker containers
make docker-down   # Stop Docker containers
make clean         # Clean Python cache files
```

## Testing

The API can be tested using:

- **Swagger UI**: Interactive API testing at `/docs`
- **ReDoc**: Alternative documentation at `/redoc`
- **Postman**: Import OpenAPI spec from `/openapi.json`
- **cURL**: Command-line testing
- **Python requests**: Programmatic testing

## Data Characteristics

The seeded data includes:

- **Realistic Names**: Generated using Faker
- **Valid VINs**: 17-character VINs
- **Consistent Dates**: Work orders distributed over 2 years
- **Business Logic**:
  - Older work orders are more likely to be completed
  - Mechanic rates vary by certification level
  - Parts have realistic pricing and warranties
  - Tax calculations are accurate
  - Odometer readings increase over time

## Roadmap

Future enhancements:

- [ ] Add POST/PUT/DELETE endpoints
- [ ] Implement rate limiting
- [ ] Add more analytics endpoints
- [ ] Support for file uploads (invoices, photos)
- [ ] Email notifications
- [ ] PDF invoice generation
- [ ] More comprehensive test suite
- [ ] GraphQL API option

## Contributing

This is a mock API project for development and testing. Feel free to fork and extend for your needs.

## License

MIT License - feel free to use this project for any purpose.

## Support

For issues or questions:
- Check the Swagger documentation at `/docs`
- Review this README
- Check application logs

## Credits

Built with:
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [Faker](https://faker.readthedocs.io/)
- [PostgreSQL](https://www.postgresql.org/)

---

**Note**: This is a mock API for development and testing purposes. All data is randomly generated and not real.
