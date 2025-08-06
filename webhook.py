import json
import logging
from flask import Request, jsonify

# Configure logging
logging.basicConfig(level=logging.INFO)

def detect_customer_anomaly(request_json):
    """Handles detectCustomerAnomaly tag."""
    parameters = {
        "anomaly_detect": "false",
        "purchase": "device protection",
        "purchase_amount": "12.25",
        "bill_without_purchase": "54.34",
        "total_bill": "66.59",
        "first_month": "January 1"
    }
    return {
        "sessionInfo": {
            "parameters": parameters
        }
    }

def validate_phone_line(request_json):
    """Handles validatePhoneLine tag."""
    parameters = {
        "domestic_coverage": "true",
        "phone_line_verified": "true"
    }
    return {
        "sessionInfo": {
            "parameters": parameters
        }
    }

def cruise_plan_coverage(request_json):
    """Handles cruisePlanCoverage tag."""
    port = request_json["sessionInfo"]["parameters"]["destination"].lower()
    
    # Hardcoded list of covered ports
    covered_ports = {
        "anguilla": True,
        "canada": True,
        "mexico": True
    }
    
    covered = "true" if port in covered_ports else "false"
    
    return {
        "sessionInfo": {
            "parameters": {
                "port_is_covered": covered
            }
        }
    }

def international_coverage(request_json):
    """Handles internationalCoverage tag."""
    destination = request_json["sessionInfo"]["parameters"]["destination"].lower()
    
    covered_monthly = {
        "anguilla": True,
        "australia": True,
        "brazil": True,
        "canada": True,
        "chile": True,
        "england": True,
        "france": True,
        "india": True,
        "japan": True,
        "mexico": True,
        "singapore": True
    }
    
    covered_daily = {
        "brazil": True,
        "canada": True,
        "chile": True,
        "england": True,
        "france": True,
        "india": True,
        "japan": True,
        "mexico": True,
        "singapore": True
    }
    
    coverage = "neither"
    monthly = destination in covered_monthly
    daily = destination in covered_daily
    
    if monthly and daily:
        coverage = "both"
    elif monthly:
        coverage = "monthly_only"
    elif daily:
        coverage = "daily_only"
    
    return {
        "sessionInfo": {
            "parameters": {
                "coverage": coverage
            }
        }
    }

def cheapest_plan(request_json):
    """Handles cheapestPlan tag."""
    return {
        "sessionInfo": {
            "parameters": {
                "monthly_cost": 70,
                "daily_cost": 100,
                "suggested_plan": "monthly"
            }
        }
    }

# Map of tag to handler functions
handlers = {
    "detectCustomerAnomaly": detect_customer_anomaly,
    "validatePhoneLine": validate_phone_line,
    "cruisePlanCoverage": cruise_plan_coverage,
    "internationalCoverage": international_coverage,
    "cheapestPlan": cheapest_plan
}

def dialogflow_cx_webhook(request: Request):
    """Entry point for Google Cloud Function"""
    try:
        request_json = request.get_json()
        logging.info(f"Request: {json.dumps(request_json, indent=2)}")
        
        tag = request_json["fulfillmentInfo"]["tag"]
        
        if tag in handlers:
            response = handlers[tag](request_json)
        else:
            raise ValueError(f"Unknown tag: {tag}")
        
        logging.info(f"Response: {json.dumps(response, indent=2)}")
        return jsonify(response)
    
    except Exception as e:
        logging.error(f"ERROR: {str(e)}")
        return jsonify({"error": str(e)}), 500
