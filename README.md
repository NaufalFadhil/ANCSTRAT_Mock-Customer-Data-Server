# Mock Customer Data Server

A lightweight REST API server built with Flask that serves mock customer data. Designed for front-end development, integration testing, and prototyping without requiring a real database.

## Features

- Paginated customer listing with configurable page size
- Customer lookup by ID
- Health check endpoint
- Docker support for containerized deployment
- JSON-file-based data store — zero database setup required

## Tech Stack

- **Python 3.12**
- **Flask 3.x** — web framework
- **Gunicorn** — production WSGI server
- **Docker** — containerization

## Project Structure

```
mock-customer-data-server/
├── app/
│   ├── app.py                  # App factory
│   ├── routes/
│   │   ├── customer_routes.py  # Customer endpoints
│   │   └── health_routes.py    # Health check endpoint
│   ├── services/
│   │   └── customer_service.py # Business logic
│   └── utils/
│       ├── json_loader.py      # Loads customer data from JSON
│       └── pagination.py       # Pagination helper
├── data/
│   └── customers.json          # Mock customer records
├── Dockerfile
├── requirements.txt
├── run.py                      # Entry point
└── .env.example
```

## Getting Started

### Prerequisites

- Python 3.12+
- pip

### Local Setup

```bash
# Clone the repository
git clone https://github.com/NaufalFadhil/ANCSTRAT_Mock-Customer-Data-Server.git mock-customer-data-server
cd mock-customer-data-server

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the development server
python run.py
```

The server will start at `http://localhost:5000`.

### Docker

```bash
# Build the image
docker build -t mock-customer-data-server .

# Run the container
docker run -p 5000:5000 --name mock-customer-data-server mock-customer-data-server
```

## API Reference

### Health Check

```
GET /api/health/
```

**Response `200`**
```json
{
  "success": true,
  "message": "Service is healty"
}
```

---

### List Customers

```
GET /api/customers/
```

**Query Parameters**

| Parameter | Type    | Default | Description               |
|-----------|---------|---------|---------------------------|
| `page`    | integer | `1`     | Page number (1-indexed)   |
| `limit`   | integer | `1`     | Number of records per page|

**Response `200`**
```json
{
  "data": [
    {
      "customer_id": "2dfc55fe-852b-4ac1-a695-659d76cb57c3",
      "first_name": "Steve",
      "last_name": "Walker",
      "email": "steve.walker@example.com",
      "phone": "+1-555-888-8888",
      "address": "678 Oak St, Anytown, USA",
      "date_of_birth": "1985-11-12",
      "account_balance": 3600.00,
      "created_at": "2023-12-01T20:00:00Z"
    }
  ],
  "total": 20,
  "page": 1,
  "limit": 1
}
```

---

### Get Customer by ID

```
GET /api/customers/<customer_id>
```

**Path Parameters**

| Parameter     | Type   | Description         |
|---------------|--------|---------------------|
| `customer_id` | string | UUID of the customer|

**Response `200`**
```json
{
  "customer_id": "2dfc55fe-852b-4ac1-a695-659d76cb57c3",
  "first_name": "Steve",
  "last_name": "Walker",
  "email": "steve.walker@example.com",
  "phone": "+1-555-888-8888",
  "address": "678 Oak St, Anytown, USA",
  "date_of_birth": "1985-11-12",
  "account_balance": 3600.00,
  "created_at": "2023-12-01T20:00:00Z"
}
```

**Response `404`**
```json
{
  "message": "Customer not found"
}
```

## Customer Data Schema

Each customer record contains the following fields:

| Field             | Type    | Description                        |
|-------------------|---------|------------------------------------|
| `customer_id`     | UUID    | Unique identifier                  |
| `first_name`      | string  | First name                         |
| `last_name`       | string  | Last name                          |
| `email`           | string  | Email address                      |
| `phone`           | string  | Phone number                       |
| `address`         | string  | Mailing address                    |
| `date_of_birth`   | date    | Date of birth (`YYYY-MM-DD`)       |
| `account_balance` | number  | Current account balance            |
| `created_at`      | datetime| Record creation timestamp (ISO 8601)|

## Environment Variables

Copy `.env.example` to `.env` and adjust as needed.

```bash
cp .env.example .env
```

| Variable    | Default | Description               |
|-------------|---------|---------------------------|
| `FLASK_ENV` | `development` | Flask environment   |
| `PORT`      | `5000`  | Port the server listens on|
