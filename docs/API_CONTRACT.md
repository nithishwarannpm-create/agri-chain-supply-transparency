# Agri-Chain Supply Transparency
# Shared API Contract

Version: 1.0
Status: Development

---

# 1. Architecture

Frontend → Backend → MongoDB
                  ↓
                  AI Service
                  ↓
                  Blockchain

Frontend communicates only with Backend.

Backend is responsible for coordinating:
- MongoDB
- AI service
- Blockchain service

---

# 2. Naming Convention

All REST API JSON fields use snake_case.

Example:

{
  "product_id": "PROD001",
  "crop_name": "Tomato"
}

Do NOT change API field names.

---

# 3. User Roles

Supported roles:

- farmer
- transporter
- distributor
- retailer
- admin

---

# 4. Product Object

A product represents an agricultural produce batch.

Example:

{
  "product_id": "PROD001",
  "crop_name": "Tomato",
  "quantity": 500,
  "unit": "kg",
  "farmer_id": "FARM001",
  "harvest_date": "2026-08-20",
  "location": "Karnataka",
  "quality_grade": "A"
}

Fields:

| Field | Type | Required |
|---|---|---|
| product_id | string | yes |
| crop_name | string | yes |
| quantity | number | yes |
| unit | string | yes |
| farmer_id | string | yes |
| harvest_date | string | yes |
| location | string | yes |
| quality_grade | string | no |

---

# 5. Product Creation API

## Request

POST /api/products

Request:

{
  "crop_name": "Tomato",
  "quantity": 500,
  "unit": "kg",
  "farmer_id": "FARM001",
  "harvest_date": "2026-08-20",
  "location": "Karnataka",
  "quality_grade": "A"
}

## Response

{
  "success": true,
  "product": {
    "product_id": "PROD001",
    "crop_name": "Tomato",
    "quantity": 500,
    "unit": "kg",
    "farmer_id": "FARM001",
    "harvest_date": "2026-08-20",
    "location": "Karnataka",
    "quality_grade": "A"
  }
}

---

# 6. Get Product

GET /api/products/{product_id}

Example:

GET /api/products/PROD001

Response:

{
  "success": true,
  "product": {
    "product_id": "PROD001",
    "crop_name": "Tomato",
    "quantity": 500,
    "unit": "kg",
    "farmer_id": "FARM001",
    "harvest_date": "2026-08-20",
    "location": "Karnataka",
    "quality_grade": "A"
  }
}

---

# 7. Supply Chain Transfer

POST /api/products/{product_id}/transfer

Request:

{
  "from_entity": "FARM001",
  "to_entity": "TRANS001",
  "location": "Bangalore",
  "timestamp": "2026-08-20T10:30:00Z"
}

Response:

{
  "success": true,
  "product_id": "PROD001",
  "transaction_id": "TX001"
}

---

# 8. Supply Chain History

GET /api/products/{product_id}/history

Response:

{
  "success": true,
  "product_id": "PROD001",
  "history": [
    {
      "from_entity": "FARM001",
      "to_entity": "TRANS001",
      "location": "Bangalore",
      "timestamp": "2026-08-20T10:30:00Z",
      "transaction_id": "TX001"
    }
  ]
}

---

# 9. AI Quality Analysis

POST /api/ai/quality

Request:

{
  "product_id": "PROD001",
  "temperature": 28.5,
  "humidity": 70,
  "moisture": 60
}

Response:

{
  "success": true,
  "product_id": "PROD001",
  "quality_score": 87.5,
  "quality_grade": "A"
}

---

# 10. AI Anomaly Detection

POST /api/ai/anomaly

Request:

{
  "product_id": "PROD001",
  "temperature": 38.5,
  "humidity": 90,
  "moisture": 85
}

Response:

{
  "success": true,
  "product_id": "PROD001",
  "anomaly_detected": true,
  "risk_score": 0.91,
  "risk_level": "HIGH",
  "anomalies": [
    "High temperature",
    "High humidity"
  ]
}

---

# 11. Blockchain Verification

GET /api/products/{product_id}/verify

Response:

{
  "success": true,
  "product_id": "PROD001",
  "verified": true,
  "transaction_id": "0x123456",
  "block_number": 123
}

---

# 12. Authentication

## Register

POST /api/auth/register

Request:

{
  "name": "Farmer One",
  "email": "farmer@example.com",
  "password": "password123",
  "role": "farmer"
}

## Login

POST /api/auth/login

Request:

{
  "email": "farmer@example.com",
  "password": "password123"
}

Response:

{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer"
}

---

# 13. Standard Error Format

All APIs must return errors in this format:

{
  "success": false,
  "error": {
    "code": "PRODUCT_NOT_FOUND",
    "message": "Product was not found"
  }
}

---

# 14. Blockchain Interface

Backend communicates with blockchain through a service/adapter.

The backend should not depend directly on Solidity variable names.

Example backend interface:

create_product(product_data)

transfer_product(product_id, transfer_data)

get_product_history(product_id)

verify_product(product_id)

Blockchain-specific names are handled inside:

backend/app/services/blockchain_service.py

---

# 15. AI Interface

Backend communicates with AI through a service/adapter.

Example:

analyze_quality(data)

detect_anomaly(data)

AI-specific variable names are handled inside:

backend/app/services/ai_service.py

---

# 16. Database Collections

MongoDB database:

agri_supply_chain

Collections:

users
products
transactions
ai_results
blockchain_records

---

# 17. Integration Rules

1. Do not rename API endpoints.
2. Do not rename JSON fields.
3. Use snake_case for API fields.
4. Frontend must communicate with Backend.
5. Frontend must not directly access MongoDB.
6. Frontend must not directly access Blockchain.
7. Backend uses adapters for AI and Blockchain.
8. AI service may use different internal variable names.
9. Blockchain may use different Solidity variable names.
10. Adapters convert between internal names and API contract names.
11. All modules must return JSON.
12. Never commit .env files.