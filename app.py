from flask import Flask, request, jsonify
from config import Config
from services.cession_calculation_service import CessionCalculationService
from services.security_service import SecurityService
from services.persistence_service import PersistenceService
import json
import uuid

app = Flask(__name__)
app.config.from_object(Config)

# Initialize services
cession_calculation_service = CessionCalculationService()
security_service = SecurityService()
persistence_service = PersistenceService()

@app.route("/api/v1/cession/calculate", methods=["POST"])
def calculate_cession():
    """
    API endpoint to calculate risk cession based on defined business rules.
    Requires HMAC authentication via 'X-Reinsurance-Hmac' header.
    """
    # 1. Security: Validate X-Reinsurance-Hmac header
    hmac_header = request.headers.get("X-Reinsurance-Hmac")
    if not hmac_header:
        return jsonify({"message": "X-Reinsurance-Hmac header is missing"}), 401

    request_body_bytes = request.get_data()
    if not security_service.validateHmacHeader(hmac_header, request_body_bytes):
        return jsonify({"message": "Invalid X-Reinsurance-Hmac header"}), 401

    # 2. Parse request body
    try:
        data = request.get_json()
        risk_id = data.get("risk_id")
        risk_amount = data.get("risk_amount")
        currency = data.get("currency")

        if not all([risk_id, risk_amount, currency]):
            return jsonify({"message": "Missing required fields: risk_id, risk_amount, currency"}), 400
        if not isinstance(risk_amount, (int, float)) or risk_amount < 0:
            return jsonify({"message": "risk_amount must be a non-negative number"}), 400

    except Exception as e:
        return jsonify({"message": f"Invalid JSON or request body: {e}"}), 400

    # 3. Calculate cession
    try:
        cession_results = cession_calculation_service.calculateCession(
            risk_id=risk_id,
            risk_amount=float(risk_amount),
            currency=currency
        )
    except Exception as e:
        app.logger.error(f"Error during cession calculation for risk_id {risk_id}: {e}")
        return jsonify({"message": "Error during cession calculation"}), 500

    # 4. Persist calculation result
    try:
        persistence_service.persistCalculationResult(
            risk_id=risk_id,
            risk_amount=float(risk_amount),
            currency=currency,
            cession_amounts=cession_results
        )
    except Exception as e:
        app.logger.error(f"Error persisting cession result for risk_id {risk_id}: {e}")
        # Decide whether to return 500 or just log and proceed.
        # For now, we'll return 500 as persistence is a critical requirement.
        return jsonify({"message": "Error persisting calculation result"}), 500

    # 5. Return response
    return jsonify(cession_results), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)