# Senco ERP - Melorra Sync Simulation API Service

A simple, Python-based API simulation service for **Senco ERP Integration with Melorra** (provisioned by Acxiom).

This service provides mock endpoints and configurable responses to simulate sales order placement and sales return sync between Melorra and Senco ERP.

---

## 🚀 Features

- **Header Authentication**: Validates hardcoded / provisioned secret key `X-Api-Key`.
- **Content-Type Validation**: Enforces `application/json`.
- **Flexible Payload Acceptance**: Accepts **any JSON payload structure** (objects, arrays, strings, custom fields) without schema restriction.
- **Port 9000**: Configured to run on port `9000` by default.
- **4 Core Simulation Endpoints**:
  1. `POST /MelorraIntegration/mel_SalesOrder` — Melorra Online Customer Sales Order insertion simulation.
  2. `POST /MelorraIntegration/mel_SalesReturn` — Melorra Sales Return & Refund processing simulation.
  3. `POST /MelorraIntegration/mel_InvoicePosting/` — Melorra Invoice Posting simulation.
  4. `POST /MelorraIntegration/mel_goldenbounty/` — Melorra Golden Bounty scheme installment posting simulation.
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

### 4. Golden Bounty Installment Endpoint
- **URL**: `POST /MelorraIntegration/mel_goldenbounty/` (also accepted without the trailing slash)
- **Request Body (JSON)** — all dates are `dd-MM-yyyy`; `fnoCustomerId` is optional (may be blank):
```json
{
  "header": {
    "company": "SGL",
    "enrolmentId": "98765",
    "enrolmentDate": "16-09-2026",
    "maturityDate": "16-08-2027",
    "tenure": "12",
    "installmentAmount": 1000,
    "copayAmount": 600,
    "maturityAmount": 12600,
    "customerId": "C2345",
    "customerName": "T Ganesha",
    "address": "H No. 56, First Floor, Mahadevpura",
    "city": "Banglore",
    "mobileNo": "9035530992",
    "emailId": "t.ganesh@Melorra.com",
    "fnoCustomerId": "CUS23451",
    "noOfInstallment": "12",
    "enrolmentStatus": "OnGoing",
    "schemeCode": "GB12",
    "schemeName": "GoldenBounty 12 Month",
    "orderLines": [
      {
        "enrolmentId": "98765",
        "enrolmentDate": "16-09-2026",
        "maturityDate": "16-08-2027",
        "installmentDate": "16-10-2026",
        "installmentAmount": 1000,
        "InstallmentNo": "2",
        "paymentDetails": [
          {
            "paymentMode": "RazorPay",
            "installmentDate": "16-10-2026",
            "amount": "1000",
            "utrNo": "UT564926761G54",
            "transactionId": "P54637221",
            "userId": "Usr1",
            "refNo": "RF67584",
            "enrolmentId": "98765"
          }
        ]
      }
    ]
  }
}
```
`header.schemeCode` is echoed back as `SchemeCode`; if it is missing, `GB-101` is returned.

**Validation**: the payload is checked against the table below (rules live in [validation.py](validation.py)) before the simulated 200/404 result is applied. Any violation returns HTTP 400 listing every failing field:
- All fields are required except `fnoCustomerId`, payment `installmentDate`, and the payment reference fields `utrNo`, `transactionId`, `refNo`, `userId` (a Cash payment has none).
- `orderLines` and each line's `paymentDetails` must contain at least one entry.
- nvarchar fields must not exceed their length; dates must be `dd-MM-yyyy`; Decimal fields must be whole numbers; Numeric(10,2) allows up to 8 digits before and 2 after the decimal point. Numbers may be sent as JSON numbers or numeric strings (`"1000"`).
- `paymentMode` must be one of `Cash`, `UPI`, `CC`, `RazorPay` (case-insensitive).

| Section | Field | Type | Length |
| :--- | :--- | :--- | :--- |
| Header | enrolmentId | nvarchar | 20 |
| Header | enrolmentDate / maturityDate | Date | 8 |
| Header | tenure | Decimal | 10 |
| Header | installmentAmount / copayAmount / maturityAmount | Numeric | 10,2 |
| Header | customerId | nvarchar | 50 |
| Header | customerName | nvarchar | 100 |
| Header | address | nvarchar | 200 |
| Header | city | nvarchar | 100 |
| Header | mobileNo | nvarchar | 20 |
| Header | emailId / fnoCustomerId | nvarchar | 50 |
| Header | noOfInstallment | Decimal | 10 |
| Header | enrolmentStatus / schemeCode / schemeName / company | nvarchar | 50 |
| Line | enrolmentId | nvarchar | 20 |
| Line | enrolmentDate / maturityDate / installmentDate | Date | 8 |
| Line | installmentAmount | Numeric | 10,2 |
| Line | InstallmentNo | Decimal | 10 |
| Payment | paymentMode (Cash/UPI/CC/RazorPay) | nvarchar | 20 |
| Payment | amount | Numeric | 10,2 |
| Payment | utrNo / userId / enrolmentId | nvarchar | 20 |
| Payment | transactionId / refNo / fnoCustomerId | nvarchar | 50 |

- **Responses**:
  - **Success (HTTP 200)**:
    ```json
    {
      "Message": "Scheme posted successfully.",
      "StatusCode": "200",
      "Status": "Success",
      "SchemeCode": "GB12"
    }
    ```
  - **Failure (HTTP 404)**:
    ```json
    {
      "Message": "Invalid Scheme code : GB12",
      "StatusCode": "404",
      "Status": "Failure",
      "SchemeCode": "GB12"
    }
    ```
  - **Validation Failure (HTTP 400)**:
    ```json
    {
      "Message": "Validation failed : header.enrolmentDate must be a date in dd-MM-yyyy format; header.customerId is required; header.orderLines[0].paymentDetails[0].utrNo exceeds max length 20 (33 chars)",
      "StatusCode": "400",
      "Status": "Failure",
      "SchemeCode": "GB12"
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
