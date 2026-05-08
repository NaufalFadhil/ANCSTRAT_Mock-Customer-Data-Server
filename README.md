# Mock Customer Data Server & Customer Pipeline Service

A two-service system for serving and ingesting mock customer data. Built for integration testing, pipeline development, and prototyping.

## Architecture

```
┌─────────────────┐        ┌──────────────────────┐        ┌──────────────┐
│   mock-server   │◄───────│  pipeline-service    │───────►│  PostgreSQL  │
│  Flask · :5000  │  HTTP  │  FastAPI · :8000     │  ORM   │    :5432     │
│  JSON file store│        │  ingestion + query   │        │              │
└─────────────────┘        └──────────────────────┘        └──────────────┘
```

- **mock-server** — Flask REST API serving customer data from a JSON file
- **pipeline-service** — FastAPI service that fetches from mock-server, upserts into Postgres, and exposes a query API
- **postgres** — Persistent store for ingested customer data

## Tech Stack

| Service          | Stack                                      |
|------------------|--------------------------------------------|
| mock-server      | Python 3.12, Flask 3.x, Gunicorn           |
| pipeline-service | Python 3.12, FastAPI, SQLAlchemy, Uvicorn  |
| database         | PostgreSQL 15                              |
| orchestration    | Docker Compose                             |

## Project Structure

```
mock-customer-data-server/
├── docker-compose.yml
├── mock-server/
│   ├── app/
│   │   ├── app.py                  # App factory
│   │   ├── routes/
│   │   │   ├── customer_routes.py
│   │   │   └── health_routes.py
│   │   ├── services/
│   │   │   └── customer_service.py
│   │   └── utils/
│   │       ├── json_loader.py
│   │       └── pagination.py
│   ├── data/
│   │   └── customers.json          # Mock customer records
│   ├── Dockerfile
│   ├── main.py                     # Entry point
│   └── requirements.txt
└── pipeline-service/
    ├── models/
    │   └── customer.py             # SQLAlchemy model
    ├── schemas/
    │   └── customer.py             # Pydantic response schema
    ├── services/
    │   └── ingestion.py            # Fetch + upsert logic
    ├── database.py                 # DB engine + session
    ├── main.py                     # FastAPI app + routes
    ├── Dockerfile
    └── requirements.txt
```

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Setup Environment

```bash
cp pipeline-service/.env.example pipeline-service/.env
```

Then edit `pipeline-service/.env` with your credentials:

```env
DATABASE_URL=postgresql://postgres:password@postgres:5432/customer_db
MOCK_SERVER_URL=http://mock-server:5000/api/customers
```

### Run with Docker Compose

```bash
# Build and start all services
docker compose up --build

# Stop and remove containers + images + volumes
docker compose down --rmi local -v
```

| Service          | URL                          |
|------------------|------------------------------|
| mock-server      | http://localhost:5000        |
| pipeline-service | http://localhost:8000        |
| postgres         | localhost:5432               |

---

## API Reference

### mock-server (port 5000)

#### Health Check

```
GET /api/health
```

**Response `200`**
```json
{
  "success": true,
  "message": "Service is healthy"
}
```

---

#### List Customers

```
GET /api/customers
```

**Query Parameters**

| Parameter | Type    | Default | Description                |
|-----------|---------|---------|----------------------------|
| `page`    | integer | `1`     | Page number (1-indexed)    |
| `limit`   | integer | `10`    | Number of records per page |

**Response `200`**
```json
{
  "data": [...],
  "total": 20,
  "page": 1,
  "limit": 10
}
```

---

#### Get Customer by ID

```
GET /api/customers/<customer_id>
```

**Response `200`** — single customer object

**Response `404`**
```json
{
  "message": "Customer not found"
}
```

---

### pipeline-service (port 8000)

#### Trigger Ingestion

```
POST /api/ingest
```

Fetches all customers from mock-server and upserts them into Postgres. No request body required.

**Response `200`**
```json
{
  "status": "success",
  "records_processed": 20
}
```

---

#### List Customers (from DB)

```
GET /api/customers
```

**Query Parameters**

| Parameter | Type    | Default | Max  | Description                |
|-----------|---------|---------|------|----------------------------|
| `page`    | integer | `1`     | —    | Page number (1-indexed)    |
| `limit`   | integer | `10`    | `100`| Number of records per page |

**Response `200`** — array of customer objects

---

#### Get Customer by ID (from DB)

```
GET /api/customers/{customer_id}
```

**Response `200`** — single customer object

**Response `404`**
```json
{
  "detail": "Customer not found"
}
```

---

## Customer Data Schema

| Field             | Type     | Description                         |
|-------------------|----------|-------------------------------------|
| `customer_id`     | UUID     | Unique identifier                   |
| `first_name`      | string   | First name                          |
| `last_name`       | string   | Last name                           |
| `email`           | string   | Email address                       |
| `phone`           | string   | Phone number                        |
| `address`         | string   | Mailing address                     |
| `date_of_birth`   | date     | Date of birth (`YYYY-MM-DD`)        |
| `account_balance` | decimal  | Current account balance             |
| `created_at`      | datetime | Record creation timestamp (ISO 8601)|

## Environment Variables

Postgres connection is configured via `DATABASE_URL` in `docker-compose.yml`.

| Variable       | Default                                              | Description             |
|----------------|------------------------------------------------------|-------------------------|
| `DATABASE_URL` | `postgresql://postgres:password@postgres:5432/customer_db` | Postgres connection string |
