from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field

# --- Customer Schema ---
class CustomerInfo(BaseModel):
    email: Optional[str] = ""
    mobileNo: Optional[str] = ""
    customerId: Optional[str] = ""
    customerName: Optional[str] = ""
    fnoCustomerId: Optional[str] = ""

# --- Address Schema ---
class AddressInfo(BaseModel):
    pin: Optional[str] = ""
    city: Optional[str] = ""
    email: Optional[str] = ""
    state: Optional[str] = ""
    address: Optional[str] = ""
    country: Optional[str] = ""
    mobileNo: Optional[str] = ""
    deliveryInstructions: Optional[str] = ""

# --- Order Header Schema ---
class OrderHeader(BaseModel):
    company: Optional[str] = "SGL"
    orderId: Optional[str] = ""
    melorraStoreCode: Optional[str] = ""
    currency: Optional[str] = "INR"
    customer: Optional[CustomerInfo] = None
    orderDate: Optional[str] = ""
    orderTime: Optional[str] = ""
    orderType: Optional[str] = "Order"
    invoiceType: Optional[str] = "Regular"
    platformId: Optional[str] = "Melorra"
    orderSource: Optional[str] = ""
    billingAddress: Optional[AddressInfo] = None
    fasterDelivery: Optional[str] = "No"
    shippingAddress: Optional[AddressInfo] = None
    totalOrderValue: Optional[float] = 0.0
    modeOfTransaction: Optional[str] = "Prepaid"

# --- Order Line Schema ---
class OrderLine(BaseModel):
    hsnCode: Optional[str] = ""
    taxRate: Optional[float] = 0
    discount: Optional[float] = 0
    itemType: Optional[str] = ""
    roundoff: Optional[float] = 0
    orderLine: Optional[str] = ""
    taxAmount: Optional[float] = 0
    designCode: Optional[str] = ""
    diamondCut: Optional[str] = ""
    goldWeight: Optional[float] = 0.0
    productQty: Optional[int] = 1
    metalPurity: Optional[str] = ""
    productSize: Optional[str] = ""
    stoneWeight: Optional[float] = 0.0
    diamondColor: Optional[str] = ""
    silverWeight: Optional[float] = 0.0
    diamondWeight: Optional[float] = 0.0
    inventBatchId: Optional[str] = ""
    makingCharges: Optional[float] = 0.0
    specialRemark: Optional[str] = ""
    RefSaleOrderNO: Optional[str] = ""
    RefSaleReturnOrderLineNo: Optional[int] = 0
    diamondClarity: Optional[str] = ""
    orderLineValue: Optional[float] = 0.0
    platinumWeight: Optional[float] = 0.0
    expectedShippingDate: Optional[str] = ""
    additionalAmount: Optional[float] = 0.0

# --- Payment Detail Schema ---
class PaymentDetail(BaseModel):
    amount: Optional[float] = 0.0
    remarks: Optional[str] = ""
    paymentId: Optional[str] = ""
    utrNumber: Optional[str] = ""
    paymentDate: Optional[str] = ""
    paymentMode: Optional[str] = ""
    employeeCode: Optional[str] = ""
    paymentStatus: Optional[str] = ""
    refDocumentNo: Optional[str] = ""
    transactionId: Optional[str] = ""
    ecomApproverId: Optional[str] = ""
    paymentGateway: Optional[str] = ""

# --- Online Customer Order Container Schema ---
class OnlineCustomerOrder(BaseModel):
    header: OrderHeader
    orderLines: Optional[List[OrderLine]] = []
    paymentDetails: Optional[List[PaymentDetail]] = []

class SalesOrderRequest(BaseModel):
    OnlineCustomerOrder: OnlineCustomerOrder

# --- Sales Return Schemas (2nd Endpoint) ---
class ReturnLine(BaseModel):
    orderLine: Optional[str] = ""
    designCode: Optional[str] = ""
    returnQty: Optional[int] = 1
    refundAmount: Optional[float] = 0.0

class ReturnHeader(BaseModel):
    company: Optional[str] = "SGL"
    returnOrderId: Optional[str] = ""
    originalOrderId: Optional[str] = ""
    melorraStoreCode: Optional[str] = ""
    customer: Optional[CustomerInfo] = None
    returnDate: Optional[str] = ""
    reason: Optional[str] = ""

class SalesReturnContainer(BaseModel):
    header: ReturnHeader
    returnLines: Optional[List[ReturnLine]] = []

class SalesReturnRequest(BaseModel):
    SalesReturnOrder: SalesReturnContainer

# --- Invoice Posting Schemas (3rd Endpoint) ---
class InvoicePostingRequest(BaseModel):
    orderNo: Optional[str] = ""
    company: Optional[str] = "SGL"
    orderLineNo: Optional[str] = ""
    tagNo: Optional[str] = ""  # In case of MTO Order Invoice
    designNo: Optional[str] = ""
    employeeCode: Optional[str] = ""
    timeStamp: Optional[str] = ""

class InvoicePostingResponse(BaseModel):
    Message: str
    StatusCode: str
    Status: str
    TagNo: str

# --- Golden Bounty Installment Schemas (4th Endpoint) ---
# Dates are dd-MM-yyyy strings
class GoldenBountyPaymentDetail(BaseModel):
    paymentMode: Optional[str] = ""  # Cash/UPI/CC/RazorPay
    installmentDate: Optional[str] = ""
    amount: Optional[float] = 0.0
    utrNo: Optional[str] = ""
    transactionId: Optional[str] = ""
    userId: Optional[str] = ""
    refNo: Optional[str] = ""
    enrolmentId: Optional[str] = ""
    fnoCustomerId: Optional[str] = ""

class GoldenBountyLine(BaseModel):
    enrolmentId: Optional[str] = ""
    enrolmentDate: Optional[str] = ""
    maturityDate: Optional[str] = ""
    installmentDate: Optional[str] = ""
    installmentAmount: Optional[float] = 0.0
    InstallmentNo: Optional[str] = ""
    paymentDetails: Optional[List[GoldenBountyPaymentDetail]] = []

class GoldenBountyHeader(BaseModel):
    company: Optional[str] = "SGL"
    enrolmentId: Optional[str] = ""
    enrolmentDate: Optional[str] = ""
    maturityDate: Optional[str] = ""
    tenure: Optional[str] = ""
    installmentAmount: Optional[float] = 0.0
    copayAmount: Optional[float] = 0.0
    maturityAmount: Optional[float] = 0.0
    customerId: Optional[str] = ""
    customerName: Optional[str] = ""
    address: Optional[str] = ""
    city: Optional[str] = ""
    mobileNo: Optional[str] = ""
    emailId: Optional[str] = ""
    fnoCustomerId: Optional[str] = ""  # Not mandatory
    noOfInstallment: Optional[str] = ""
    enrolmentStatus: Optional[str] = ""
    schemeCode: Optional[str] = ""
    schemeName: Optional[str] = ""
    orderLines: Optional[List[GoldenBountyLine]] = []

class GoldenBountyRequest(BaseModel):
    header: GoldenBountyHeader

class GoldenBountyResponse(BaseModel):
    Message: str
    StatusCode: str
    Status: str
    SchemeCode: str

# --- Response Schema ---
class IntegrationResponse(BaseModel):
    Message: str
    StatusCode: str
    OrderId: str

# --- Dynamic Simulation Config Schema ---
class SimulationConfigUpdate(BaseModel):
    default_status: str  # "200" or "404"
    failure_message: Optional[str] = None
    success_message: Optional[str] = None
    api_key: Optional[str] = None
