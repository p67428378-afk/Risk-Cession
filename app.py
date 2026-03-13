"""
Module: app
Purpose: Main Flask application for the Risk Cession Calculation Service.
Author: Your Name
Created: 2023-10-27
Notes: Exposes the /api/v1/cession/calculate endpoint and integrates services.
"""

from flask import Flask, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
import logging

from config import Config
from database import SessionLocal, init_db
from services.cession_calculation_service import CessionCalculationService
from services.security_service import SecurityService
from services.persistence_service import PersistenceService

app = Flask(__name__)
app.config.from_object(Config)

# Initialize services
cession_calculator = CessionCalculationService()
security_service = SecurityService()
persistence_service = PersistenceService()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.before_request
def before_request_func():
    """
    Initializes a new database session before each request.
    """
    request.db = SessionLocal()

@app.after_request
def after_request_func(response):
    """
    Closes the database session after each request.
    """
    if hasattr(request, 'db'):
        request.db.close()
    return response

@app.route("/api/v1/cession/calculate", methods=["POST"])
def calculate_cession():
    """
    API endpoint to calculate risk cession.
    Validates HMAC header, performs calculation, and persists results.
    """
    # 1. Security: Validate X-Reinsurance-Hmac header
    hmac_header = request.headers.get("X-Reinsurance-Hmac")
    if not security_service.validate_hmac_header(hmac_header, request.data):
        logging.warning("Unauthorized access attempt: Invalid HMAC header.")
        return jsonify({"message": "Unauthorized: Invalid HMAC header"}), 401

    # 2. Input Validation
    try:
        data = request.get_json(force=True) # force=True will try to parse even if content-type is not application/json
    except Exception as e:
        logging.error(f"Bad Request: Invalid JSON data or content type. Error: {e}")
        return jsonify({"message": "Bad Request: Invalid JSON data or content type"}), 400

    if not data:
        logging.error("Bad Request: No JSON data provided or empty JSON.")
        return jsonify({"message": "Bad Request: No JSON data provided"}), 400

    risk_id = data.get("risk_id")
    risk_amount = data.get("risk_amount")
    currency = data.get("currency")

    if not all([risk_id, isinstance(risk_amount, (int, float)), currency]):
        logging.error(f"Bad Request: Missing or invalid parameters. Data: {data}")
        return jsonify({
            "message": "Bad Request: Missing or invalid parameters. "
                       "Required: 'risk_id' (string), 'risk_amount' (number), 'currency' (string)"
        }), 400

    if risk_amount < 0:
        logging.error(f"Bad Request: risk_amount cannot be negative. Value: {risk_amount}")
        return jsonify({"message": "Bad Request: 'risk_amount' cannot be negative"}), 400

    try:
        # 3. Calculate Cession
        cession_results = cession_calculator.calculate_cession(risk_id, risk_amount, currency)

        # 4. Persist Calculation Result
        # For now, reinsurer_details is an empty dict as it's not explicitly defined in the model
        # but kept for HLD compliance in method signature.
        persistence_service.persist_calculation_result(
            db=request.db,
            risk_id=risk_id,
            risk_amount=risk_amount,
            currency=currency,
            cession_amounts=cession_results,
            reinsurer_details={}
        )
        logging.info(f"Cession calculation and persistence successful for risk_id: {risk_id}")
        return jsonify(cession_results), 200

    except SQLAlchemyError as e:
        request.db.rollback()
        logging.exception(f"Database error during cession calculation for risk_id: {risk_id}")
        return jsonify({"message": f"Internal Server Error: Database operation failed. {str(e)}"}), 500
    except Exception as e:
        logging.exception(f"An unexpected error occurred during cession calculation for risk_id: {risk_id}")
        return jsonify({"message": f"Internal Server Error: {str(e)}"}), 500

if __name__ == "__main__":
    init_db() # Ensure tables are created on startup
    app.run(host="0.0.0.0", port=5000, debug=True)
