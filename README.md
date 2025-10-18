
# Streamoid Product Catalog Backend

This project is a backend service for uploading, validating, storing, and searching product catalogs as described in the Streamoid submission task.

## Features & Requirements

- **Upload CSV**: `POST /upload` — Accepts a CSV file of products, validates each row (required fields, price ≤ mrp, quantity ≥ 0), and stores valid products in a SQLite database. Duplicate SKUs are rejected and reported in the response.
- **List Products**: `GET /products` — Returns all stored products with pagination (`page`, `limit`).
- **Search/Filter Products**: `GET /products/search` — Filter by brand, color, and price range (`minPrice`, `maxPrice`).
- **Validation**: Ensures all required fields are present and valid. Duplicate SKUs are not inserted and are reported as failed.
- **Unit Tests**: Includes tests for CSV parsing and validation.
- **Dockerized**: Includes a Dockerfile for easy deployment.

## API Endpoints

### 1. Upload Products CSV
**POST** `/upload`

Form-data: `file` (CSV file)

**Response Example:**
```json
{
	"stored": 3,
	"failed": [
		{"sku": "TSHIRT-RED-001", "errors": ["duplicate_or_constraint_error"]}
	]
}
```

### 2. List Products
**GET** `/products?page=1&limit=10`

**Response Example:**
```json
{
	"total": 2,
	"page": 1,
	"limit": 10,
	"items": [
		{
			"sku": "TSHIRT-RED-001",
			"name": "Classic Cotton T-Shirt",
			"brand": "Stream Threads",
			"color": "Red",
			"size": "M",
			"mrp": 799,
			"price": 499,
			"quantity": 20
		}
	]
}
```

### 3. Search Products
**GET** `/products/search?brand=StreamThreads&minPrice=500&maxPrice=2000`

**Response Example:**
```json
[
	{
		"sku": "TSHIRT-RED-001",
		"name": "Classic Cotton T-Shirt",
		"brand": "Stream Threads",
		"color": "Red",
		"size": "M",
		"mrp": 799,
		"price": 499,
		"quantity": 20
	}
]
```

## Setup & Running

### Local (Windows)
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

### Docker
```bash
docker run -p 8000:8000 streamoid-app
```

## Testing

Run unit tests:
```cmd
python tests\run_tests.py
```


---
