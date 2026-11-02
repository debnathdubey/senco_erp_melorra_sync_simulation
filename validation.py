import re
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, List

# Field rules for the Golden Bounty payload, taken from the Acxiom table structure.
# Each rule is (field, kind, size, required):
#   "str"     -> nvarchar(size)
#   "date"    -> dd-MM-yyyy string
#   "decimal" -> Decimal(size), whole number with up to `size` digits
#   "numeric" -> Numeric(precision, scale), e.g. (10, 2)
#   "enum"    -> one of the listed values
GOLDEN_BOUNTY_HEADER_RULES = [
    ("company", "str", 50, True),
    ("enrolmentId", "str", 20, True),
    ("enrolmentDate", "date", None, True),
    ("maturityDate", "date", None, True),
    ("tenure", "decimal", 10, True),
    ("installmentAmount", "numeric", (10, 2), True),
    ("copayAmount", "numeric", (10, 2), True),
    ("maturityAmount", "numeric", (10, 2), True),
    ("customerId", "str", 50, True),
    ("customerName", "str", 100, True),
    ("address", "str", 200, True),
    ("city", "str", 100, True),
    ("mobileNo", "str", 20, True),
    ("emailId", "str", 50, True),
    ("fnoCustomerId", "str", 50, False),  # Not mandatory, may be blank
    ("noOfInstallment", "decimal", 10, True),
    ("enrolmentStatus", "str", 50, True),
    ("schemeCode", "str", 50, True),
    ("schemeName", "str", 50, True),
]

GOLDEN_BOUNTY_LINE_RULES = [
    ("enrolmentId", "str", 20, True),
    ("enrolmentDate", "date", None, True),
    ("maturityDate", "date", None, True),
    ("installmentDate", "date", None, True),
    ("installmentAmount", "numeric", (10, 2), True),
    ("InstallmentNo", "decimal", 10, True),
]

PAYMENT_MODES = ["Cash", "UPI", "CC", "RazorPay"]

# utrNo / transactionId / refNo / userId are optional since a Cash payment has none of them
GOLDEN_BOUNTY_PAYMENT_RULES = [
    ("paymentMode", "enum", PAYMENT_MODES, True),
    ("installmentDate", "date", None, False),
    ("amount", "numeric", (10, 2), True),
    ("utrNo", "str", 20, False),
    ("transactionId", "str", 50, False),
    ("userId", "str", 20, False),
    ("refNo", "str", 50, False),
    ("enrolmentId", "str", 20, True),
    ("fnoCustomerId", "str", 50, False),
]

DATE_PATTERN = re.compile(r"^\d{2}-\d{2}-\d{4}$")


def _to_decimal(value: Any):
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        return None
    try:
        d = Decimal(str(value).strip())
    except InvalidOperation:
        return None
    return d if d.is_finite() else None


def _check_field(path: str, value: Any, kind: str, size: Any) -> List[str]:
    if kind == "str":
        if isinstance(value, bool) or not isinstance(value, (str, int)):
            return [f"{path} must be text"]
        if len(str(value)) > size:
            return [f"{path} exceeds max length {size} ({len(str(value))} chars)"]

    elif kind == "date":
        if not isinstance(value, str) or not DATE_PATTERN.match(value):
            return [f"{path} must be a date in dd-MM-yyyy format"]
        try:
            datetime.strptime(value, "%d-%m-%Y")
        except ValueError:
            return [f"{path} is not a valid date"]

    elif kind == "decimal":
        d = _to_decimal(value)
        if d is None or d != d.to_integral_value() or len(str(abs(int(d)))) > size:
            return [f"{path} must be a whole number with up to {size} digits"]

    elif kind == "numeric":
        precision, scale = size
        d = _to_decimal(value)
        exponent = d.as_tuple().exponent if d is not None else 0
        if (d is None
                or max(0, -exponent) > scale
                or len(str(abs(int(d)))) > precision - scale):
            return [f"{path} must be a number with up to {precision - scale} digits "
                    f"before and {scale} after the decimal point"]

    elif kind == "enum":
        if not isinstance(value, str) or value.lower() not in [v.lower() for v in size]:
            return [f"{path} must be one of {', '.join(size)}"]

    return []


def _check_object(path: str, obj: Any, rules) -> List[str]:
    if not isinstance(obj, dict):
        return [f"{path} must be an object"]
    errors = []
    for field, kind, size, required in rules:
        value = obj.get(field)
        field_path = f"{path}.{field}"
        if value is None or value == "":
            if required:
                errors.append(f"{field_path} is required")
            continue
        errors.extend(_check_field(field_path, value, kind, size))
    return errors


def _check_list(path: str, value: Any) -> List[str]:
    if not isinstance(value, list) or not value:
        return [f"{path} must be a list with at least one entry"]
    return []


def validate_golden_bounty(body: Any) -> List[str]:
    """Returns every rule violation in a Golden Bounty payload; empty if valid."""
    if not isinstance(body, dict) or "header" not in body:
        return ["header is required"]

    header = body["header"]
    errors = _check_object("header", header, GOLDEN_BOUNTY_HEADER_RULES)
    if not isinstance(header, dict):
        return errors

    lines = header.get("orderLines")
    list_errors = _check_list("header.orderLines", lines)
    if list_errors:
        return errors + list_errors

    for i, line in enumerate(lines):
        line_path = f"header.orderLines[{i}]"
        errors.extend(_check_object(line_path, line, GOLDEN_BOUNTY_LINE_RULES))
        if not isinstance(line, dict):
            continue
        payments = line.get("paymentDetails")
        list_errors = _check_list(f"{line_path}.paymentDetails", payments)
        if list_errors:
            errors.extend(list_errors)
            continue
        for j, payment in enumerate(payments):
            errors.extend(_check_object(f"{line_path}.paymentDetails[{j}]", payment,
                                        GOLDEN_BOUNTY_PAYMENT_RULES))
    return errors
