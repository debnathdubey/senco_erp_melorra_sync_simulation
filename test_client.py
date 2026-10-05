#!/usr/bin/env python3
import argparse
import json
import os
import requests
import sys

parser = argparse.ArgumentParser(description="Test client for Senco ERP Melorra Simulation API")
parser.add_argument("--port", type=int, default=int(os.getenv("PORT", "9000")), help="Port of the server (default: 9000)")
parser.add_argument("--host", type=str, default="127.0.0.1", help="Host of the server (default: 127.0.0.1)")
args, _ = parser.parse_known_args()

BASE_URL = f"http://{args.host}:{args.port}"
API_KEY = os.getenv("X_API_KEY", "Acxiom-Melorra-Secret-Key-2026")

sales_order_payload = {
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

sales_return_payload = {
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


def run_tests():
    print("==================================================")
    print(" RUNNING SENCO ERP - MELORRA SIMULATION TESTS")
    print("==================================================")

    headers_valid = {
        "X-Api-Key": API_KEY,
        "Content-Type": "application/json"
    }

    # Test 1: Sales Order Success (200)
    print("\n[TEST 1] POST /MelorraIntegration/mel_SalesOrder (Success 200 Mode)...")
    res = requests.post(f"{BASE_URL}/MelorraIntegration/mel_SalesOrder", headers=headers_valid, json=sales_order_payload)
    print(f"HTTP Status: {res.status_code}")
    print(f"Response: {json.dumps(res.json(), indent=2)}")

    # Test 2: Sales Order Failure Override (404)
    print("\n[TEST 2] POST /MelorraIntegration/mel_SalesOrder (Overridden Failure 404 Mode)...")
    headers_fail = dict(headers_valid)
    headers_fail["X-Simulate-Status"] = "404"
    res = requests.post(f"{BASE_URL}/MelorraIntegration/mel_SalesOrder", headers=headers_fail, json=sales_order_payload)
    print(f"HTTP Status: {res.status_code}")
    print(f"Response: {json.dumps(res.json(), indent=2)}")

    # Test 3: Invalid API Key (401)
    print("\n[TEST 3] POST /MelorraIntegration/mel_SalesOrder (Invalid API Key)...")
    headers_invalid_key = {
        "X-Api-Key": "INVALID_KEY_123",
        "Content-Type": "application/json"
    }
    res = requests.post(f"{BASE_URL}/MelorraIntegration/mel_SalesOrder", headers=headers_invalid_key, json=sales_order_payload)
    print(f"HTTP Status: {res.status_code}")
    print(f"Response: {json.dumps(res.json(), indent=2)}")

    # Test 4: Sales Return Endpoint 2 Success (200)
    print("\n[TEST 4] POST /MelorraIntegration/mel_SalesReturn (Endpoint 2)...")
    res = requests.post(f"{BASE_URL}/MelorraIntegration/mel_SalesReturn", headers=headers_valid, json=sales_return_payload)
    print(f"HTTP Status: {res.status_code}")
    print(f"Response: {json.dumps(res.json(), indent=2)}")

    print("\n==================================================")
    print(" ALL TESTS COMPLETED")
    print("==================================================")

if __name__ == "__main__":
    run_tests()
