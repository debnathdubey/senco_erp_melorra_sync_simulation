# Senco ERP - Melorra Sync Simulation API Service

A simple, Python-based API simulation service for **Senco ERP Integration with Melorra** (provisioned by Acxiom).

This service provides mock endpoints and configurable responses to simulate sales order placement and sales return sync between Melorra and Senco ERP.

---

## 🚀 Features

- **Header Authentication**: Validates hardcoded / provisioned secret key `X-Api-Key`.
- **Content-Type Validation**: Enforces `application/json`.
- **Flexible Payload Acceptance**: Accepts **any JSON payload structure** (objects, arrays, strings, custom fields) without schema restriction.
- **Port 9000**: Configured to run on port `9000` by default.
- **3 Core Simulation Endpoints**:
  1. `POST /MelorraIntegration/mel_SalesOrder` — Melorra Online Customer Sales Order insertion simulation.
  2. `POST /MelorraIntegration/mel_SalesReturn` — Melorra Sales Return & Refund processing simulation.
  3. `POST /MelorraIntegration/mel_InvoicePosting/` — Melorra Invoice Posting simulation.
- **Dynamic Simulation Controls**:
  - Switch global server response mode between `200 OK (Success)` and `404 Not Found (Failure)`.
  - Override response mode per-request using `X-Simulate-Status: 200` or `X-Simulate-Status: 404` header or `?simulate_status=404` query parameter.
- **Web Dashboard**: Interactive glassmorphism dashboard UI (`http://localhost:9000/`) with real-time request logging, simulation controls, and one-click test execution.
- **Swagger Documentation**: Interactive OpenAPI docs available at `http://localhost:9000/docs`.

---

## 🔑 Header Requirements

| Header Name | Required | Value / Description |
| :--- | :--- | :--- |
| `X-Api-Key` | **Yes** | Shared secret key provisioned by Acxiom. Default: `Acxiom-Melorra-Secret-Key-2026` |
| `Content-Type` | **Yes** | `application/json` |
| `X-Simulate-Status` | *Optional* | Set `200` or `404` to force a specific response status for testing. |

---

## 📌 API Endpoints

### 1. Sales Order Endpoint
- **URL**: `POST /MelorraIntegration/mel_SalesOrder`
- **Request Body (JSON)**:
```json
{
  "OnlineCustomerOrder": {
    "header": {
      "company": "SGL",
      "orderId": "TSGDIND0000000060861",
      "melorraStoreCode": "M766PMC27",
      "currency": "INR",
      "customer": {
        "email": "subhasis@mobotics.in",
        "mobileNo": "7595958418",
        "customerId": "12CUS000068",
        "customerName": "Subhasis Das",
        "fnoCustomerId": "12CUS000068"
      },
      "orderDate": "04-08-2026",
      "orderTime": "10:56:33",
      "orderType": "Order",
      "invoiceType": "Regular",
      "platformId": "Melorra",
      "orderSource": "",
      "billingAddress": {
        "pin": "700008",
        "city": "Kolkata",
        "email": "subhasis@mobotics.in",
        "state": "WB",
        "address": "64/2/45 Biren Roy Road,east Kolkata 700008",
        "country": "IND",
        "mobileNo": "7595958418"
      },
      "fasterDelivery": "No",
      "shippingAddress": {
        "pin": "700008",
        "city": "Kolkata",
        "email": "dsubhasis934@gmail.com",
        "state": "WB",
        "address": "64/2/45 Biren Roy Road,east Kolkata 700008",
        "country": "IND",
        "mobileNo": "7595958418",
        "deliveryInstructions": ""
      },
      "totalOrderValue": 23132,
      "modeOfTransaction": "Prepaid"
    },
    "orderLines": [
      {
        "hsnCode": "",
        "taxRate": 3,
        "discount": 0,
        "itemType": "DIAMOND",
        "roundoff": 0,
        "orderLine": "84471",
        "taxAmount": 413,
        "designCode": "DPN-D000528006",
        "diamondCut": "",
        "goldWeight": 1.322,
        "productQty": 1,
        "metalPurity": "14K",
        "productSize": "",
        "stoneWeight": 0,
        "diamondColor": "",
        "silverWeight": 0,
        "diamondWeight": 0.19,
        "inventBatchId": "DPN006481173",
        "makingCharges": 2200,
        "specialRemark": "",
        "RefSaleOrderNO": "",
        "RefSaleReturnOrderLineNo": 0,
        "diamondClarity": "HI-SI",
        "orderLineValue": 23132,
        "platinumWeight": 0,
        "expectedShippingDate": "04-08-2026",
        "additionalAmount": 0
      }
    ],
    "paymentDetails": [
      {
        "amount": 23132,
        "remarks": "Manual UTR entry by OA",
        "paymentId": "order_TLZonnZL5MdNYI",
        "utrNumber": "TSGDIND0000000060861",
        "paymentDate": "04-08-2026",
        "paymentMode": "Online Payment",
        "employeeCode": "",
        "paymentStatus": "Success",
        "refDocumentNo": "",
        "transactionId": "order_TLZonnZL5MdNYI",
        "ecomApproverId": "",
        "paymentGateway": "Online"
      }
    ]
  }
}
```

- **Responses**:
  - **Success (HTTP 200)**:
    ```json
    {
      "Message": "Sales order inserted successfully.",
      "StatusCode": "200",
      "OrderId": "ORD98756"
    }
    ```
  - **Failure (HTTP 404)**:
    ```json
    {
      "Message": "Sales order insertion is failed. - Tag no: UTY75674 is not released",
      "StatusCode": "404",
      "OrderId": "ORD98756"
    }
    ```
  - **Unauthorized (HTTP 401)**:
    ```json
    {
      "Message": "Authentication failed: Invalid or missing X-Api-Key header.",
      "StatusCode": "401",
      "OrderId": ""
    }
    ```

---

### 2. Sales Return Endpoint
- **URL**: `POST /MelorraIntegration/mel_SalesReturn`
- **Request Body (JSON)**:
```json
{
  "SalesReturnOrder": {
    "header": {
      "company": "SGL",
      "returnOrderId": "RET-TSGDIND0000000060861",
      "originalOrderId": "TSGDIND0000000060861",
      "melorraStoreCode": "M766PMC27",
      "customer": {
        "customerId": "12CUS000068",
        "customerName": "Subhasis Das"
      },
      "returnDate": "05-08-2026",
      "reason": "Customer Return - Size issue"
    },
    "returnLines": [
      {
        "orderLine": "84471",
        "designCode": "DPN-D000528006",
        "returnQty": 1,
        "refundAmount": 23132
      }
    ]
  }
}
```

- **Responses**:
  - **Success (HTTP 200)**:
    ```json
    {
      "Message": "Sales return processed successfully.",
      "StatusCode": "200",
      "OrderId": "RET-RET-TSGDIND0000000060861"
    }
    ```
  - **Failure (HTTP 404)**:
    ```json
    {
      "Message": "Sales return processing failed. - Original order line not released for return",
      "StatusCode": "404",
      "OrderId": "RET-RET-TSGDIND0000000060861"
    }
    ```

---

### 3. Invoice Posting Endpoint
- **URL**: `POST /MelorraIntegration/mel_InvoicePosting/` (also accepted without the trailing slash)
- **Request Body (JSON)**:
```json
{
  "orderNo": "ONORD-1506-0001",
  "company": "SGL",
  "orderLineNo": "1",
  "tagNo": "BB1006480937",
  "designNo": "BB1-D000144073",
  "employeeCode": "",
  "timeStamp": ""
}
```
`tagNo` is sent in case of an MTO Order Invoice. When present it is echoed back as `TagNo`; otherwise a generated tag number is returned.

- **Responses**:
  - **Success (HTTP 200)**:
    ```json
    {
      "Message": "Invoice posted successfully.",
      "StatusCode": "200",
      "Status": "Success",
      "TagNo": "BB1006480937"
    }
    ```
  - **Failure (HTTP 404)**:
    ```json
    {
      "Message": "Invalid order id : BB1-D000144073",
      "StatusCode": "404",
      "Status": "Failure",
      "TagNo": "BB1006480937"
    }
    ```

---

## ⚙️ How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Server
```bash
python3 -m uvicorn main:app --host 0.0.0.0 --port 9000 --reload
```
Or simply:
```bash
python3 main.py
```

### 3. Open Web Dashboard & Documentation
- Web Dashboard: [http://localhost:9000/](http://localhost:9000/)
- Swagger API Docs: [http://localhost:9000/docs](http://localhost:9000/docs)
- Health Check: [http://localhost:9000/MelorraIntegration/health](http://localhost:9000/MelorraIntegration/health)

---

## 🧪 Testing

Run the included automated test suite:
```bash
python3 test_client.py
```

Or using **cURL**:

#### Success Request:
```bash
curl -X POST "http://127.0.0.1:9000/MelorraIntegration/mel_SalesOrder" \
  -H "X-Api-Key: Acxiom-Melorra-Secret-Key-2026" \
  -H "Content-Type: application/json" \
  -d '{
    "OnlineCustomerOrder": {
      "header": { "orderId": "TSGDIND0000000060861" }
    }
  }'
```

#### Simulate Failure (404) via Header:
```bash
curl -X POST "http://127.0.0.1:9000/MelorraIntegration/mel_SalesOrder" \
  -H "X-Api-Key: Acxiom-Melorra-Secret-Key-2026" \
  -H "X-Simulate-Status: 404" \
  -H "Content-Type: application/json" \
  -d '{
    "OnlineCustomerOrder": {
      "header": { "orderId": "TSGDIND0000000060861" }
    }
  }'
```
