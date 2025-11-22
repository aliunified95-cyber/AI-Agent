import pdfplumber
import re
import json
from typing import Dict, Any, Optional
from app.models.order import OrderData, OrderType, LineType, FinancialType, Customer, LineDetails, Device, Plan, Financial

def parse_order_pdf(pdf_path: str) -> Dict[str, Any]:
    """
    Parse order summary PDF and extract structured data
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        if not text:
            raise ValueError("No text extracted from PDF")
        
        # Extract order data
        order_data = {
            "order_id": extract_order_id(text),
            "customer": extract_customer_info(text),
            "order_type": extract_order_type(text),
            "line_details": extract_line_details(text),
            "device": extract_device_info(text),
            "plan": extract_plan_info(text),
            "financial": extract_financial_info(text),
            "accessories": extract_accessories(text),
            "credit_control_options": []
        }
        
        return order_data
    except Exception as e:
        raise Exception(f"Error parsing PDF: {str(e)}")

def extract_order_id(text: str) -> str:
    """Extract order ID from text"""
    patterns = [
        r'Order\s+ID[:\s]+(\d{4}-\d{4}-\d+)',
        r'Order\s+Number[:\s]+(\d{4}-\d{4}-\d+)',
        r'(\d{4}-\d{4}-\d+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
    
    return "UNKNOWN-ORDER-ID"

def extract_customer_info(text: str) -> Dict[str, str]:
    """Extract customer information"""
    customer = {
        "name": "",
        "cpr": "",
        "mobile": "",
        "preferred_language": None
    }
    
    # Name patterns
    name_patterns = [
        r'Customer\s+Name[:\s]+(.+?)(?:\n|CPR|Mobile)',
        r'Name[:\s]+(.+?)(?:\n|CPR|Mobile)',
        r'Full\s+Name[:\s]+(.+?)(?:\n|CPR|Mobile)',
    ]
    
    for pattern in name_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            customer["name"] = match.group(1).strip()
            break
    
    # CPR patterns
    cpr_patterns = [
        r'CPR[:\s]+(\d{9})',
        r'CPR\s+Number[:\s]+(\d{9})',
        r'ID\s+Number[:\s]+(\d{9})',
    ]
    
    for pattern in cpr_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            customer["cpr"] = match.group(1)
            break
    
    # Mobile patterns
    mobile_patterns = [
        r'Mobile[:\s]+(\d{8})',
        r'Phone[:\s]+(\d{8})',
        r'Contact[:\s]+(\d{8})',
    ]
    
    for pattern in mobile_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            customer["mobile"] = match.group(1)
            break
    
    return customer

def extract_order_type(text: str) -> str:
    """Extract order type"""
    text_lower = text.lower()
    
    if "new line" in text_lower or "newline" in text_lower:
        return "new_line"
    elif "existing line" in text_lower or "existingline" in text_lower:
        return "existing_line"
    elif "cash" in text_lower:
        return "cash"
    
    return "new_line"  # Default

def extract_line_details(text: str) -> Dict[str, str]:
    """Extract line details"""
    line_details = {
        "type": "mobile",
        "number": None,
        "sub_number": None
    }
    
    # Check for fiber
    if "fiber" in text.lower():
        line_details["type"] = "fiber"
    
    # Extract line numbers
    number_patterns = [
        r'Line\s+Number[:\s]+(\d{8})',
        r'Number[:\s]+(\d{8})',
        r'Existing\s+Number[:\s]+(\d{8})',
    ]
    
    for pattern in number_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            line_details["number"] = match.group(1)
            break
    
    # Extract sub-number
    sub_number_patterns = [
        r'Sub[-\s]?Number[:\s]+(\d{8})',
        r'New\s+Number[:\s]+(\d{8})',
    ]
    
    for pattern in sub_number_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            line_details["sub_number"] = match.group(1)
            break
    
    return line_details

def extract_device_info(text: str) -> Optional[Dict[str, str]]:
    """Extract device information"""
    device_patterns = [
        r'Device[:\s]+(.+?)(?:\n|Plan|Package|Financial)',
        r'Product[:\s]+(.+?)(?:\n|Plan|Package|Financial)',
    ]
    
    for pattern in device_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            device_str = match.group(1).strip()
            # Try to parse device details
            parts = device_str.split()
            if len(parts) >= 2:
                return {
                    "name": device_str,
                    "variant": parts[-1] if len(parts) > 1 else "",
                    "color": ""
                }
    
    return None

def extract_plan_info(text: str) -> Optional[Dict[str, str]]:
    """Extract plan information"""
    plan_patterns = [
        r'Plan[:\s]+(.+?)(?:\n|Commitment|Financial)',
        r'Package[:\s]+(.+?)(?:\n|Commitment|Financial)',
    ]
    
    plan_name = None
    for pattern in plan_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            plan_name = match.group(1).strip()
            break
    
    # Extract commitment period
    commitment_patterns = [
        r'Commitment[:\s]+(\d{1,2})\s*month',
        r'(\d{1,2})[-\s]month',
    ]
    
    commitment = "24"  # Default
    for pattern in commitment_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            commitment = match.group(1)
            break
    
    if plan_name:
        return {
            "name": plan_name,
            "selected_commitment": commitment
        }
    
    return None

def extract_financial_info(text: str) -> Dict[str, Any]:
    """Extract financial information"""
    financial = {
        "type": "INSTALLMENT",
        "monthly": 0.0,
        "advance": 0.0,
        "upfront": 0.0,
        "vat": 0.0,
        "total": 0.0
    }
    
    # Check financial type
    if "subsidy" in text.lower():
        financial["type"] = "SUBSIDY"
    
    # Extract amounts (look for numbers with "BD", "Dinar", or currency symbols)
    amount_patterns = [
        r'Monthly[:\s]+(\d+\.?\d*)',
        r'Advance[:\s]+(\d+\.?\d*)',
        r'Upfront[:\s]+(\d+\.?\d*)',
        r'VAT[:\s]+(\d+\.?\d*)',
        r'Total[:\s]+(\d+\.?\d*)',
    ]
    
    financial["monthly"] = extract_amount(text, "Monthly")
    financial["advance"] = extract_amount(text, "Advance")
    financial["upfront"] = extract_amount(text, "Upfront")
    financial["vat"] = extract_amount(text, "VAT")
    financial["total"] = extract_amount(text, "Total")
    
    return financial

def extract_amount(text: str, label: str) -> float:
    """Extract amount for a specific label"""
    patterns = [
        rf'{label}[:\s]+(\d+\.?\d*)',
        rf'{label}\s+Payment[:\s]+(\d+\.?\d*)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return float(match.group(1))
    
    return 0.0

def extract_accessories(text: str) -> List[str]:
    """Extract accessories list"""
    accessories = []
    
    # Look for accessories section
    accessory_pattern = r'Accessories?[:\s]+(.+?)(?:\n\n|\n[A-Z])'
    match = re.search(accessory_pattern, text, re.IGNORECASE)
    
    if match:
        accessories_str = match.group(1)
        # Split by common delimiters
        accessories = [a.strip() for a in re.split(r'[,;]', accessories_str) if a.strip()]
    
    return accessories

