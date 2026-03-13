# Risk Cession Calculation Service

This service calculates risk cession based on defined business rules, enabling accurate management of reinsurance treaties and financial exposure. It exposes a REST API endpoint for calculations, validates requests using an HMAC header, and persists results to a database.

## Features

- **API Endpoint**: `POST /api/v1/cession/calculate` for risk cession calculations.
- **Risk Layers**: Implements Retention, Proportional, and Excess of Loss (XOL) layers.
- **Security**: Validates `X-Reinsurance-Hmac` header for request authenticity.
- **Persistence**: Stores calculation results in a database (in-memory for this implementation).
- **Modularity**: Uses a Strategy Pattern for easy addition of new reinsurers.

## Setup and Installation

### Prerequisites

- Python 3.9+
- Docker (optional, for containerized deployment)

### Local Development

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/p67428378-afk/Risk-Cession.git
    cd Risk-Cession
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Create a `.env` file:**

    Copy the `.env.example` file to `.env` and update the `HMAC_SECRET_KEY`.

    ```bash
    cp .env.example .env
    ```

    Edit `.env`:

    ```
    HMAC_SECRET_KEY=your_super_secret_key_here
    ```

5.  **Run the Flask application:**

    ```bash
    flask run --host=0.0.0.0
    ```

    The service will be available at `http://127.0.0.1:5000`.

### Docker Deployment

1.  **Build the Docker image:**

    ```bash
    docker build -t risk-cession-service .
    ```

2.  **Run the Docker container:**

    ```bash
    docker run -p 5000:5000 -e HMAC_SECRET_KEY="your_super_secret_key_here" risk-cession-service
    ```

    The service will be available at `http://localhost:5000`.

## API Usage

### `POST /api/v1/cession/calculate`

Calculates the risk cession based on the provided risk details.

**Headers:**

-   `Content-Type: application/json`
-   `X-Reinsurance-Hmac`: HMAC-SHA256 signature of the request body, signed with `HMAC_SECRET_KEY`.

**Request Body Example:**

```json
{
    "risk_id": "RISK-001",
    "risk_amount": 150000000,
    "currency": "USD"
}
```

**Response Body Example (Success):**

```json
{
    "currency": "USD",
    "global_re_group_cession": 100000000,
    "reinsurer_a_cession": 0,
    "retention": 50000000,
    "risk_amount": 150000000,
    "risk_id": "RISK-001"
}
```

**Error Responses:**

-   `400 Bad Request`: Invalid JSON, missing parameters, or invalid parameter types.
-   `401 Unauthorized`: Missing or invalid `X-Reinsurance-Hmac` header.
-   `500 Internal Server Error`: Server misconfiguration (e.g., `HMAC_SECRET_KEY` not set).

## Testing the HMAC Signature (Example using Python)

You can generate the `X-Reinsurance-Hmac` header using a Python script:

```python
import hmac
import hashlib
import json
import requests

SECRET_KEY = "your_super_secret_key_here" # Must match the one in your .env or Docker env
API_URL = "http://127.0.0.1:5000/api/v1/cession/calculate"

request_payload = {
    "risk_id": "RISK-001",
    "risk_amount": 150000000,
    "currency": "USD"
}

json_payload = json.dumps(request_payload)

hmac_signature = hmac.new(SECRET_KEY.encode('utf-8'), json_payload.encode('utf-8'), hashlib.sha256).hexdigest()

headers = {
    "Content-Type": "application/json",
    "X-Reinsurance-Hmac": hmac_signature
}

response = requests.post(API_URL, headers=headers, data=json_payload)

print(f"Status Code: {response.status_code}")
print(f"Response Body: {response.json()}")
```
