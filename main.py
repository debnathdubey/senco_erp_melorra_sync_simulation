import os
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, Header, HTTPException, Request, Response, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse

from config import DEFAULT_API_KEY
from schemas import (
    SalesOrderRequest,
    SalesReturnRequest,
    IntegrationResponse,
    SimulationConfigUpdate
)

app = FastAPI(
    title="Senco ERP - Melorra Sync Simulation API",
    description="Simulated Python API service for Acxiom-Senco ERP Melorra integration",
    version="1.0.0"
)

# Enable CORS for convenience in testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Simulation State
simulation_state = {
    "api_key": DEFAULT_API_KEY,
    "default_status": "200",  # "200" for success, "404" for failure
    "success_message": "Sales order inserted successfully.",
    "failure_message": "Sales order insertion is failed. - Tag no: UTY75674 is not released",
    "order_id_counter": 98756,
}

# In-memory Request Logs for debugging & UI display
request_logs: List[Dict[str, Any]] = []
MAX_LOGS = 100


def log_request(endpoint: str, headers: Dict[str, str], payload: Dict[str, Any], response: Dict[str, Any], status_code: int):
    log_entry = {
        "id": len(request_logs) + 1,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "endpoint": endpoint,
        "api_key_used": headers.get("x-api-key", "MISSING"),
        "status_code": status_code,
        "payload": payload,
        "response": response
    }
    request_logs.insert(0, log_entry)
    if len(request_logs) > MAX_LOGS:
        request_logs.pop()


def verify_api_key(x_api_key: Optional[str] = Header(None, alias="X-Api-Key")):
    """Verifies the X-Api-Key header against configured secret key."""
    expected_key = simulation_state["api_key"]
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "Message": "Authentication failed: Missing X-Api-Key header.",
                "StatusCode": "401",
                "OrderId": ""
            }
        )
    if x_api_key != expected_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "Message": f"Authentication failed: Invalid X-Api-Key '{x_api_key}'.",
                "StatusCode": "401",
                "OrderId": ""
            }
        )
    return x_api_key


# ==========================================
# ENDPOINT 1: POST /MelorraIntegration/mel_SalesOrder
# ==========================================
@app.post("/MelorraIntegration/mel_SalesOrder", tags=["Melorra Integration"])
async def create_sales_order(
    request: Request,
    x_api_key: Optional[str] = Header(None, alias="X-Api-Key"),
    x_simulate_status: Optional[str] = Header(None, alias="X-Simulate-Status"),
    simulate_status: Optional[str] = Query(None)
):
    """
    Simulates inserting a Sales Order from Melorra into Senco ERP (Acxiom integration).
    Accepts ANY valid JSON payload.
    """
    # Accept any JSON structure (object, array, primitive, etc.)
    try:
        body = await request.json()
    except Exception:
        try:
            raw_bytes = await request.body()
            body = {"raw_content": raw_bytes.decode("utf-8", errors="ignore")}
        except Exception:
            body = {}

    # Verify Content-Type
    content_type = request.headers.get("content-type", "")
    if "application/json" not in content_type.lower():
        resp = {
            "Message": "Invalid Content-Type. Expected application/json",
            "StatusCode": "400",
            "OrderId": ""
        }
        log_request("/MelorraIntegration/mel_SalesOrder", dict(request.headers), body, resp, 400)
        return JSONResponse(status_code=400, content=resp)

    # Validate Auth Key
    expected_key = simulation_state["api_key"]
    if not x_api_key or x_api_key != expected_key:
        resp = {
            "Message": "Authentication failed: Invalid or missing X-Api-Key header.",
            "StatusCode": "401",
            "OrderId": ""
        }
        log_request("/MelorraIntegration/mel_SalesOrder", dict(request.headers), body, resp, 401)
        return JSONResponse(status_code=401, content=resp)

    # Determine simulation result (Header > Query param > Server Default)
    target_status = x_simulate_status or simulate_status or simulation_state["default_status"]

    # Extract Order ID if present in body, or fallback to default ORD98756
    order_id = "ORD98756"
    if isinstance(body, dict):
        try:
            header_data = body.get("OnlineCustomerOrder", {}).get("header", {})
            input_order_id = header_data.get("orderId") if isinstance(header_data, dict) else None
            if input_order_id:
                order_id = f"ORD{simulation_state['order_id_counter']}"
        except Exception:
            pass

    if str(target_status) == "200":
        response_data = {
            "Message": simulation_state["success_message"],
            "StatusCode": "200",
            "OrderId": order_id
        }
        http_status = 200
    else:
        response_data = {
            "Message": simulation_state["failure_message"],
            "StatusCode": "404",
            "OrderId": order_id
        }
        http_status = 404

    log_request("/MelorraIntegration/mel_SalesOrder", dict(request.headers), body, response_data, http_status)
    return JSONResponse(status_code=http_status, content=response_data)


# ==========================================
# ENDPOINT 2: POST /MelorraIntegration/mel_SalesReturn
# ==========================================
@app.post("/MelorraIntegration/mel_SalesReturn", tags=["Melorra Integration"])
async def create_sales_return(
    request: Request,
    x_api_key: Optional[str] = Header(None, alias="X-Api-Key"),
    x_simulate_status: Optional[str] = Header(None, alias="X-Simulate-Status"),
    simulate_status: Optional[str] = Query(None)
):
    """
    Simulates processing a Sales Return / Cancellation order from Melorra into Senco ERP.
    Accepts ANY valid JSON payload.
    """
    try:
        body = await request.json()
    except Exception:
        try:
            raw_bytes = await request.body()
            body = {"raw_content": raw_bytes.decode("utf-8", errors="ignore")}
        except Exception:
            body = {}

    content_type = request.headers.get("content-type", "")
    if "application/json" not in content_type.lower():
        resp = {
            "Message": "Invalid Content-Type. Expected application/json",
            "StatusCode": "400",
            "OrderId": ""
        }
        log_request("/MelorraIntegration/mel_SalesReturn", dict(request.headers), body, resp, 400)
        return JSONResponse(status_code=400, content=resp)

    expected_key = simulation_state["api_key"]
    if not x_api_key or x_api_key != expected_key:
        resp = {
            "Message": "Authentication failed: Invalid or missing X-Api-Key header.",
            "StatusCode": "401",
            "OrderId": ""
        }
        log_request("/MelorraIntegration/mel_SalesReturn", dict(request.headers), body, resp, 401)
        return JSONResponse(status_code=401, content=resp)

    target_status = x_simulate_status or simulate_status or simulation_state["default_status"]
    
    order_id = "RET98756"
    if isinstance(body, dict):
        try:
            ret_header = body.get("SalesReturnOrder", {}).get("header", {})
            if isinstance(ret_header, dict) and ret_header.get("returnOrderId"):
                order_id = f"RET-{ret_header.get('returnOrderId')}"
        except Exception:
            pass

    if str(target_status) == "200":
        response_data = {
            "Message": "Sales return processed successfully.",
            "StatusCode": "200",
            "OrderId": order_id
        }
        http_status = 200
    else:
        response_data = {
            "Message": "Sales return processing failed. - Original order line not released for return",
            "StatusCode": "404",
            "OrderId": order_id
        }
        http_status = 404

    log_request("/MelorraIntegration/mel_SalesReturn", dict(request.headers), body, response_data, http_status)
    return JSONResponse(status_code=http_status, content=response_data)


# ==========================================
# HEALTH & CONTROL APIS
# ==========================================
@app.get("/MelorraIntegration/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "service": "Senco ERP Melorra Integration Simulation",
        "current_simulation_mode": simulation_state["default_status"],
        "api_key_configured": simulation_state["api_key"],
        "time": datetime.now().isoformat()
    }


@app.get("/api/simulation/config", tags=["Simulation Control"])
async def get_config():
    return simulation_state


@app.post("/api/simulation/config", tags=["Simulation Control"])
async def update_config(update: SimulationConfigUpdate):
    if update.default_status in ["200", "404"]:
        simulation_state["default_status"] = update.default_status
    if update.failure_message:
        simulation_state["failure_message"] = update.failure_message
    if update.success_message:
        simulation_state["success_message"] = update.success_message
    if update.api_key:
        simulation_state["api_key"] = update.api_key
    return {"status": "updated", "config": simulation_state}


@app.get("/api/simulation/logs", tags=["Simulation Control"])
async def get_logs():
    return request_logs


@app.delete("/api/simulation/logs", tags=["Simulation Control"])
async def clear_logs():
    request_logs.clear()
    return {"message": "Logs cleared successfully"}


# ==========================================
# WEB DASHBOARD (HTML UI)
# ==========================================
@app.get("/", response_class=HTMLResponse, tags=["Dashboard"])
async def serve_dashboard():
    api_key = simulation_state["api_key"]
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Senco ERP - Melorra Sync Simulation Dashboard</title>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-dark: #0f172a;
      --card-bg: rgba(30, 41, 59, 0.7);
      --card-border: rgba(255, 255, 255, 0.1);
      --accent-gold: #f59e0b;
      --accent-emerald: #10b981;
      --accent-rose: #f43f5e;
      --accent-cyan: #06b6d4;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
      background: radial-gradient(circle at 15% 15%, #1e1b4b 0%, #0f172a 60%);
      color: var(--text-main);
      min-height: 100vh;
      padding: 24px;
    }}

    header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 24px;
      border-bottom: 1px solid var(--card-border);
      margin-bottom: 28px;
    }}

    .logo-area {{
      display: flex;
      align-items: center;
      gap: 16px;
    }}

    .badge {{
      background: linear-gradient(135deg, #d97706, #f59e0b);
      color: #000;
      font-weight: 700;
      padding: 4px 12px;
      border-radius: 20px;
      font-size: 0.8rem;
      letter-spacing: 0.5px;
      text-transform: uppercase;
    }}

    h1 {{
      font-size: 1.6rem;
      font-weight: 700;
      background: linear-gradient(to right, #fbbf24, #f43f5e, #38bdf8);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    .sub {{
      color: var(--text-muted);
      font-size: 0.9rem;
      margin-top: 2px;
    }}

    .grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
    }}

    @media (max-width: 1024px) {{
      .grid {{
        grid-template-columns: 1fr;
      }}
    }}

    .card {{
      background: var(--card-bg);
      backdrop-filter: blur(12px);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 24px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }}

    .card-title {{
      font-size: 1.2rem;
      font-weight: 600;
      margin-bottom: 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}

    .status-toggle {{
      display: flex;
      background: rgba(15, 23, 42, 0.8);
      border-radius: 12px;
      padding: 4px;
      border: 1px solid var(--card-border);
    }}

    .status-btn {{
      border: none;
      padding: 8px 18px;
      border-radius: 8px;
      font-weight: 600;
      cursor: pointer;
      font-size: 0.9rem;
      transition: all 0.2s ease;
      color: var(--text-muted);
      background: transparent;
    }}

    .status-btn.active-200 {{
      background: var(--accent-emerald);
      color: #fff;
      box-shadow: 0 0 12px rgba(16, 185, 129, 0.4);
    }}

    .status-btn.active-404 {{
      background: var(--accent-rose);
      color: #fff;
      box-shadow: 0 0 12px rgba(244, 63, 94, 0.4);
    }}

    .field-group {{
      margin-bottom: 16px;
    }}

    label {{
      display: block;
      font-size: 0.85rem;
      color: var(--text-muted);
      margin-bottom: 6px;
      font-weight: 500;
    }}

    input[type="text"], textarea {{
      width: 100%;
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid var(--card-border);
      border-radius: 8px;
      padding: 10px 14px;
      color: var(--text-main);
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.88rem;
    }}

    input:focus, textarea:focus {{
      outline: none;
      border-color: var(--accent-cyan);
      box-shadow: 0 0 0 2px rgba(6, 182, 212, 0.2);
    }}

    .btn {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 10px 20px;
      border-radius: 8px;
      font-weight: 600;
      cursor: pointer;
      border: none;
      transition: all 0.2s;
      font-size: 0.9rem;
    }}

    .btn-primary {{
      background: linear-gradient(135deg, #0284c7, #2563eb);
      color: #fff;
    }}

    .btn-primary:hover {{
      transform: translateY(-1px);
      box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4);
    }}

    .btn-success {{
      background: linear-gradient(135deg, #059669, #10b981);
      color: #fff;
    }}

    .btn-outline {{
      background: transparent;
      border: 1px solid var(--card-border);
      color: var(--text-main);
    }}

    .btn-outline:hover {{
      background: rgba(255, 255, 255, 0.05);
    }}

    pre {{
      font-family: 'JetBrains Mono', monospace;
      background: #090d16;
      border: 1px solid rgba(255, 255, 255, 0.05);
      border-radius: 10px;
      padding: 14px;
      font-size: 0.82rem;
      overflow-x: auto;
      max-height: 360px;
    }}

    .log-item {{
      border-bottom: 1px solid var(--card-border);
      padding: 12px 0;
    }}

    .log-header {{
      display: flex;
      justify-content: space-between;
      margin-bottom: 6px;
      font-size: 0.85rem;
    }}

    .pill {{
      padding: 2px 8px;
      border-radius: 6px;
      font-size: 0.75rem;
      font-weight: 700;
    }}

    .pill-200 {{ background: rgba(16, 185, 129, 0.2); color: #34d399; }}
    .pill-404 {{ background: rgba(244, 63, 94, 0.2); color: #fb7185; }}
    .pill-401 {{ background: rgba(245, 158, 11, 0.2); color: #fbbf24; }}

    .endpoint-badge {{
      font-family: 'JetBrains Mono', monospace;
      background: rgba(255, 255, 255, 0.08);
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 0.82rem;
    }}
  </style>
</head>
<body>

  <header>
    <div class="logo-area">
      <div>
        <h1>SENCO ERP x MELORRA API SIMULATOR</h1>
        <div class="sub">Acxiom Integration Simulation Engine & Response Control</div>
      </div>
    </div>
    <div style="text-align: right;">
      <span class="badge">PROVISIONED BY ACXIOM</span>
    </div>
  </header>

  <div class="grid">
    <!-- LEFT COLUMN: CONTROLS & TEST CLIENT -->
    <div style="display: flex; flex-direction: column; gap: 24px;">
      
      <!-- Simulation Config Card -->
      <div class="card">
        <div class="card-title">
          <span>Simulation Status Mode</span>
          <div class="status-toggle">
            <button id="btn-200" class="status-btn active-200" onclick="setMode('200')">200 SUCCESS</button>
            <button id="btn-404" class="status-btn" onclick="setMode('404')">404 FAILURE</button>
          </div>
        </div>
        
        <div class="field-group">
          <label>Configured X-Api-Key Header (Hardcoded Secret)</label>
          <input type="text" id="api-key-input" value="{api_key}">
        </div>

        <div class="field-group">
          <label>Failure Response Message (when 404 mode active)</label>
          <input type="text" id="failure-msg-input" value="Sales order insertion is failed. - Tag no: UTY75674 is not released">
        </div>

        <div style="display: flex; gap: 12px; margin-top: 12px;">
          <button class="btn btn-primary" onclick="saveConfig()">Save Configuration</button>
        </div>
      </div>

      <!-- Endpoints Tester Card -->
      <div class="card">
        <div class="card-title">
          <span>Interactive Test Client</span>
        </div>

        <div class="field-group">
          <label>Select Endpoint to Test</label>
          <select id="test-endpoint-select" style="width: 100%; background: #0f172a; color: #fff; border: 1px solid var(--card-border); padding: 10px; border-radius: 8px;" onchange="updatePayloadTemplate()">
            <option value="/MelorraIntegration/mel_SalesOrder">POST /MelorraIntegration/mel_SalesOrder (Endpoint 1)</option>
            <option value="/MelorraIntegration/mel_SalesReturn">POST /MelorraIntegration/mel_SalesReturn (Endpoint 2)</option>
          </select>
        </div>

        <div class="field-group">
          <label>Test Header X-Api-Key</label>
          <input type="text" id="test-key-input" value="{api_key}">
        </div>

        <div class="field-group">
          <label>Request JSON Payload</label>
          <textarea id="test-payload-input" rows="10"></textarea>
        </div>

        <div style="display: flex; gap: 12px;">
          <button class="btn btn-success" onclick="sendTestRequest()">Send Request</button>
          <button class="btn btn-outline" onclick="copyCurl()">Copy cURL</button>
        </div>

        <div style="margin-top: 16px;">
          <label>Response</label>
          <pre id="test-response-output">// Click 'Send Request' to execute</pre>
        </div>
      </div>

    </div>

    <!-- RIGHT COLUMN: LIVE LOGS & API SPECIFICATION -->
    <div style="display: flex; flex-direction: column; gap: 24px;">
      
      <!-- API Endpoints Info Card -->
      <div class="card">
        <div class="card-title">Available Endpoints</div>
        
        <div style="display: flex; flex-direction: column; gap: 12px;">
          <div style="background: rgba(15, 23, 42, 0.6); padding: 12px; border-radius: 10px; border: 1px solid var(--card-border);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span class="endpoint-badge" style="color: #38bdf8;">POST /MelorraIntegration/mel_SalesOrder</span>
              <span style="font-size: 0.75rem; color: var(--text-muted);">Endpoint 1</span>
            </div>
            <div style="font-size: 0.82rem; color: var(--text-muted); margin-top: 6px;">
              Insert Online Customer Sales Order into ERP
            </div>
          </div>

          <div style="background: rgba(15, 23, 42, 0.6); padding: 12px; border-radius: 10px; border: 1px solid var(--card-border);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span class="endpoint-badge" style="color: #f472b6;">POST /MelorraIntegration/mel_SalesReturn</span>
              <span style="font-size: 0.75rem; color: var(--text-muted);">Endpoint 2</span>
            </div>
            <div style="font-size: 0.82rem; color: var(--text-muted); margin-top: 6px;">
              Process Sales Return & Customer Refunds in ERP
            </div>
          </div>
        </div>
      </div>

      <!-- Live Request Logs Card -->
      <div class="card">
        <div class="card-title">
          <span>Live Request History</span>
          <button class="btn btn-outline" style="font-size: 0.75rem; padding: 4px 10px;" onclick="clearLogs()">Clear Logs</button>
        </div>

        <div id="logs-container" style="max-height: 520px; overflow-y: auto;">
          <div style="color: var(--text-muted); font-size: 0.9rem;">No requests logged yet.</div>
        </div>
      </div>

    </div>
  </div>

  <script>
    const sampleSalesOrder = {{
      "OnlineCustomerOrder": {{
        "header": {{
          "company": "SGL",
          "orderId": "TSGDIND0000000060861",
          "melorraStoreCode": "M766PMC27",
          "currency": "INR",
          "customer": {{
            "email": "subhasis@mobotics.in",
            "mobileNo": "7595958418",
            "customerId": "12CUS000068",
            "customerName": "Subhasis Das",
            "fnoCustomerId": "12CUS000068"
          }},
          "orderDate": "04-08-2026",
          "orderTime": "10:56:33",
          "orderType": "Order",
          "invoiceType": "Regular",
          "platformId": "Melorra",
          "orderSource": "",
          "billingAddress": {{
            "pin": "700008",
            "city": "Kolkata",
            "email": "subhasis@mobotics.in",
            "state": "WB",
            "address": "64/2/45 Biren Roy Road,east Kolkata 700008",
            "country": "IND",
            "mobileNo": "7595958418"
          }},
          "fasterDelivery": "No",
          "shippingAddress": {{
            "pin": "700008",
            "city": "Kolkata",
            "email": "dsubhasis934@gmail.com",
            "state": "WB",
            "address": "64/2/45 Biren Roy Road,east Kolkata 700008",
            "country": "IND",
            "mobileNo": "7595958418",
            "deliveryInstructions": ""
          }},
          "totalOrderValue": 23132,
          "modeOfTransaction": "Prepaid"
        }},
        "orderLines": [
          {{
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
          }}
        ],
        "paymentDetails": [
          {{
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
          }}
        ]
      }}
    }};

    const sampleSalesReturn = {{
      "SalesReturnOrder": {{
        "header": {{
          "company": "SGL",
          "returnOrderId": "RET-TSGDIND0000000060861",
          "originalOrderId": "TSGDIND0000000060861",
          "melorraStoreCode": "M766PMC27",
          "customer": {{
            "customerId": "12CUS000068",
            "customerName": "Subhasis Das"
          }},
          "returnDate": "05-08-2026",
          "reason": "Customer Return - Size issue"
        }},
        "returnLines": [
          {{
            "orderLine": "84471",
            "designCode": "DPN-D000528006",
            "returnQty": 1,
            "refundAmount": 23132
          }}
        ]
      }}
    }};

    function updatePayloadTemplate() {{
      const select = document.getElementById('test-endpoint-select');
      const payloadArea = document.getElementById('test-payload-input');
      if (select.value.includes('mel_SalesReturn')) {{
        payloadArea.value = JSON.stringify(sampleSalesReturn, null, 2);
      }} else {{
        payloadArea.value = JSON.stringify(sampleSalesOrder, null, 2);
      }}
    }}

    async function setMode(status) {{
      document.getElementById('btn-200').className = status === '200' ? 'status-btn active-200' : 'status-btn';
      document.getElementById('btn-404').className = status === '404' ? 'status-btn active-404' : 'status-btn';
      await saveConfig(status);
    }}

    async function saveConfig(forcedStatus) {{
      const status = forcedStatus || (document.getElementById('btn-200').classList.contains('active-200') ? '200' : '404');
      const apiKey = document.getElementById('api-key-input').value;
      const failMsg = document.getElementById('failure-msg-input').value;

      try {{
        const res = await fetch('/api/simulation/config', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{
            default_status: status,
            api_key: apiKey,
            failure_message: failMsg
          }})
        }});
        const data = await res.json();
        document.getElementById('test-key-input').value = apiKey;
      }} catch (err) {{
        console.error("Failed to update config:", err);
      }}
    }}

    async function sendTestRequest() {{
      const endpoint = document.getElementById('test-endpoint-select').value;
      const apiKey = document.getElementById('test-key-input').value;
      const payloadStr = document.getElementById('test-payload-input').value;
      const output = document.getElementById('test-response-output');

      output.textContent = "Sending request...";

      try {{
        let parsedPayload = JSON.parse(payloadStr);
        const res = await fetch(endpoint, {{
          method: 'POST',
          headers: {{
            'Content-Type': 'application/json',
            'X-Api-Key': apiKey
          }},
          body: JSON.stringify(parsedPayload)
        }});

        const data = await res.json();
        output.textContent = `HTTP ${{res.status}}\n` + JSON.stringify(data, null, 2);
        fetchLogs();
      }} catch (err) {{
        output.textContent = "Error: " + err.message;
      }}
    }}

    function copyCurl() {{
      const endpoint = document.getElementById('test-endpoint-select').value;
      const apiKey = document.getElementById('test-key-input').value;
      const payloadStr = document.getElementById('test-payload-input').value.replace(/'/g, "'\\\\''");
      const url = window.location.origin + endpoint;
      const curl = `curl -X POST "${{url}}" \\\n  -H "X-Api-Key: ${{apiKey}}" \\\n  -H "Content-Type: application/json" \\\n  -d '${{payloadStr}}'`;
      
      navigator.clipboard.writeText(curl);
      alert("cURL command copied to clipboard!");
    }}

    async function fetchLogs() {{
      try {{
        const res = await fetch('/api/simulation/logs');
        const logs = await res.json();
        const container = document.getElementById('logs-container');

        if (logs.length === 0) {{
          container.innerHTML = '<div style="color: var(--text-muted); font-size: 0.9rem;">No requests logged yet.</div>';
          return;
        }}

        container.innerHTML = logs.map(log => `
          <div class="log-item" style="border-bottom: 1px solid var(--card-border); padding: 14px 0;">
            <div class="log-header">
              <span><strong>${{log.endpoint}}</strong></span>
              <span class="pill pill-${{log.status_code}}">HTTP ${{log.status_code}}</span>
            </div>
            <div style="font-size: 0.78rem; color: var(--text-muted); margin-bottom: 8px;">
              ${{log.timestamp}} | Key: <code>${{log.api_key_used}}</code>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 6px;">
              <div>
                <div style="font-size: 0.75rem; font-weight: 600; color: #38bdf8; margin-bottom: 4px;">📥 Incoming Request Payload</div>
                <pre style="max-height: 180px; padding: 8px 10px; font-size: 0.75rem; background: #070a12; border-radius: 6px;">${{JSON.stringify(log.payload, null, 2)}}</pre>
              </div>
              <div>
                <div style="font-size: 0.75rem; font-weight: 600; color: #34d399; margin-bottom: 4px;">📤 Simulated Response</div>
                <pre style="max-height: 180px; padding: 8px 10px; font-size: 0.75rem; background: #070a12; border-radius: 6px;">${{JSON.stringify(log.response, null, 2)}}</pre>
              </div>
            </div>
          </div>
        `).join('');
      }} catch (err) {{
        console.error("Failed to fetch logs:", err);
      }}
    }}

    async function clearLogs() {{
      await fetch('/api/simulation/logs', {{ method: 'DELETE' }});
      fetchLogs();
    }}

    // Init
    updatePayloadTemplate();
    fetchLogs();
    setInterval(fetchLogs, 5000);
  </script>
</body>
</html>
"""


if __name__ == "__main__":
    import argparse
    import uvicorn
    from config import HOST, PORT

    parser = argparse.ArgumentParser(description="Senco ERP - Melorra Sync Simulation API Service")
    parser.add_argument("--port", type=int, default=PORT, help=f"Port to run server on (default: {PORT})")
    parser.add_argument("--host", type=str, default=HOST, help=f"Host address to bind to (default: {HOST})")
    args = parser.parse_args()

    print(f"Starting Senco ERP Melorra Simulation Server on http://{args.host}:{args.port}")
    uvicorn.run("main:app", host=args.host, port=args.port, reload=True)

