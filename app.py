from flask import Flask, request, jsonify
from config import Config
from security import SecurityService
from cession_calculator import CessionCalculationService
from persistence import PersistenceService
import hmac
import hashlib

app = Flask(__name__)
app.config.from_object(Config)

# Initialize services
security_service = SecurityService()
cession_calculation_service = CessionCalculationService()
persistence_service = PersistenceService()

@app.before_request
def validate_hmac_header():
    # Only apply HMAC validation to the cession calculation endpoint
    if request.path == '/api/v1/cession/calculate':
        hmac_header = request.headers.get('X-Reinsurance-Hmac')
        if not hmac_header:
            app.logger.warning("HMAC header missing for /api/v1/cession/calculate")
            return jsonify({"message": "X-Reinsurance-Hmac header missing"}), 401

        secret_key = app.config.get('SECRET_KEY')
        if not secret_key:
            app.logger.error("HMAC_SECRET_KEY not configured in Config.")
            return jsonify({"message": "Server security misconfiguration"}), 500

        # Reconstruct the message body for HMAC validation
        # It's crucial that the client sends the exact same body used to generate the HMAC
        message_body = request.get_data()

        # Generate expected HMAC
        expected_hmac = hmac.new(secret_key.encode('utf-8'), message_body, hashlib.sha256).hexdigest()

        # Compare using a constant-time comparison to prevent timing attacks
        if not hmac.compare_digest(expected_hmac, hmac_header):
            app.logger.warning(f"Invalid HMAC header for /api/v1/cession/calculate. Expected: {expected_hmac}, Received: {hmac_header}")
            return jsonify({"message": "Invalid X-Reinsurance-Hmac header"}), 401
    
    # If not the target path, or if validation passes, continue to the route handler
    pass

@app.route('/api/v1/cession/calculate', methods=['POST'])
def calculate_cession():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid JSON payload"}), 400

    risk_id = data.get('risk_id')
    risk_amount = data.get('risk_amount')
    currency = data.get('currency')

    # Input validation
    if not all([risk_id, risk_amount, currency]):
        return jsonify({"message": "Missing required parameters: risk_id, risk_amount, currency"}), 400
    
    if not isinstance(risk_id, str):
        return jsonify({"message": "risk_id must be a string"}), 400
    if not isinstance(risk_amount, (int, float)) or risk_amount < 0:
        return jsonify({"message": "risk_amount must be a non-negative number"}), 400
    if not isinstance(currency, str):
        return jsonify({"message": "currency must be a string"}), 400

    # Calculate cession
    cession_results = cession_calculation_service.calculateCession(risk_id, float(risk_amount), currency)

    # Prepare data for persistence as per HLD Section 11.1 PersistenceService.persistCalculationResult
    reinsurer_details = {
        "Reinsurer A": {"cession_amount": cession_results["reinsurer_a_cession"]},
        "Global Re Group": {"cession_amount": cession_results["global_re_group_cession"]}
    }
    persistence_service.persistCalculationResult(
        risk_id=risk_id,
        risk_amount=float(risk_amount),
        currency=currency,
        cession_amounts={
            "retention": cession_results["retention"],
            "reinsurer_a_cession": cession_results["reinsurer_a_cession"],
            "global_re_group_cession": cession_results["global_re_group_cession"]
        },
        reinsurer_details=reinsurer_details
    )

    # Return response as per HLD Section 11.3 Data Schemas (Response)
    return jsonify(cession_results), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
