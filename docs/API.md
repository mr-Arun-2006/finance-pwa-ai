# API Documentation

## Base URL

```
http://localhost:3001/api
```

## Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <token>
```

## Endpoints

### Authentication

#### Register User

```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword",
  "firstName": "John",
  "lastName": "Doe"
}
```

**Response:**
```json
{
  "id": "user-id",
  "email": "user@example.com",
  "token": "jwt-token"
}
```

#### Login

```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "token": "jwt-token",
  "user": {
    "id": "user-id",
    "email": "user@example.com"
  }
}
```

### Transactions

#### Get All Transactions

```http
GET /transactions?page=1&limit=20&startDate=2024-01-01&endDate=2024-12-31
Authorization: Bearer <token>
```

**Response:**
```json
{
  "transactions": [
    {
      "id": "txn-id",
      "date": "2024-01-15",
      "amount": 45.99,
      "description": "Grocery Store",
      "category": "Groceries",
      "merchant": "Walmart"
    }
  ],
  "total": 150,
  "page": 1,
  "pages": 8
}
```

#### Create Transaction

```http
POST /transactions
Authorization: Bearer <token>
Content-Type: application/json

{
  "date": "2024-01-15",
  "amount": 45.99,
  "description": "Grocery Shopping",
  "category": "Groceries",
  "merchant": "Walmart",
  "paymentMethod": "credit_card"
}
```

#### Upload CSV

```http
POST /transactions/upload/csv
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: <csv-file>
```

### Budgets

#### Get All Budgets

```http
GET /budgets
Authorization: Bearer <token>
```

**Response:**
```json
{
  "budgets": [
    {
      "id": "budget-id",
      "category": "Groceries",
      "limit": 500,
      "spent": 325,
      "remaining": 175,
      "month": "2024-01"
    }
  ]
}
```

#### Create Budget

```http
POST /budgets
Authorization: Bearer <token>
Content-Type: application/json

{
  "category": "Groceries",
  "limit": 500,
  "month": "2024-01"
}
```

#### Update Budget

```http
PUT /budgets/:id
Authorization: Bearer <token>
Content-Type: application/json

{
  "limit": 600
}
```

### Forecasts

#### Get Spending Forecast

```http
GET /forecasts?days=30&category=Groceries
Authorization: Bearer <token>
```

**Response:**
```json
{
  "forecast": [
    {
      "date": "2024-02-01",
      "predicted_amount": 450,
      "confidence_lower": 380,
      "confidence_upper": 520
    }
  ],
  "trend": "increasing",
  "average": 450
}
```

#### Detect Anomalies

```http
GET /forecasts/anomalies/detect
Authorization: Bearer <token>
```

**Response:**
```json
{
  "anomalies": [
    {
      "date": "2024-01-20",
      "amount": 1500,
      "description": "Large purchase detected",
      "severity": "high"
    }
  ]
}
```

### Analytics

#### Get Dashboard Analytics

```http
GET /analytics/dashboard
Authorization: Bearer <token>
```

**Response:**
```json
{
  "balance": 12450,
  "monthly_spending": 3240,
  "daily_average": 108,
  "savings_rate": 0.32,
  "top_categories": [
    {"category": "Groceries", "amount": 450},
    {"category": "Transportation", "amount": 320}
  ]
}
```

#### Get Spending Trends

```http
GET /analytics/trends?period=monthly
Authorization: Bearer <token>
```

## Error Responses

### 400 Bad Request

```json
{
  "error": "Invalid input",
  "details": "Amount must be greater than 0"
}
```

### 401 Unauthorized

```json
{
  "error": "Unauthorized",
  "message": "Invalid or expired token"
}
```

### 404 Not Found

```json
{
  "error": "Resource not found"
}
```

### 500 Internal Server Error

```json
{
  "error": "Internal server error",
  "message": "Something went wrong"
}
```

## Rate Limiting

- **Rate Limit**: 100 requests per 15 minutes per IP
- **Headers**: 
  - `X-RateLimit-Limit`: 100
  - `X-RateLimit-Remaining`: Remaining requests
  - `X-RateLimit-Reset`: Reset time (Unix timestamp)

## Pagination

All list endpoints support pagination:

- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20, max: 100)

## Sorting

Supported sort fields depend on endpoint. Use `sort` parameter:

```
GET /transactions?sort=-date&sort=+amount
```

- `-` for descending
- `+` for ascending
