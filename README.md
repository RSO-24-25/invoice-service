# Invoice Service

## Overview
The Invoice Service is a microservice for generating PDF invoices and logging invoice activities to a serverless function. It provides endpoints to create invoices and monitor service health.

## Features
- **Invoice Generation**: Creates PDF invoices with details such as sender, receiver, and transaction amount.
- **Activity Logging**: Sends invoice data to a serverless function for logging into a Firestore database.
- **Health Check**: Provides a status endpoint for monitoring the service.

---

## Architecture
The service interacts with a serverless function for logging invoice data and uses the following stack:
- **Framework**: FastAPI for the main service, Flask for serverless function.
- **PDF Generation**: FPDF library.
- **Logging**: Google Cloud Firestore.

---

## Setup Instructions

### Prerequisites
- Python 3.9 or higher
- Docker
- Google Cloud service account credentials (JSON file)

### Installation
1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd invoice-service
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set environment variables in `.env`:
    ```bash
    SERVERLESS_FUNCTION_URL="https://log-activity-1059882736634.us-central1.run.app"
    PDF_DIRECTORY="./invoices"
    ```

4. Build and run with Docker Compose:
    ```bash
    docker-compose up --build
    ```

---

## Usage

### Endpoints

| Method | Endpoint            | Description                  |
|--------|---------------------|------------------------------|
| POST   | `/generate-invoice` | Generates a PDF invoice and logs data to the serverless function. |
| GET    | `/status`           | Returns the service status.  |

### Example Request (Invoice Generation)
#### Request:
```json
POST /generate-invoice
Content-Type: application/json

{
  "sender_name": "Alice",
  "receiver_name": "Bob",
  "amount": 150.00
}
