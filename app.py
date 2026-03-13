from flask import Flask, request, jsonify
import json
from services.cession_calculation_service import CessionCalculationService
from services.security_service import SecurityService
from services.persistence_service import PersistenceService
from models.cession_result import CessionResult

app = Flask(__name__)

cession_calculation_service = CessionCalculationService()
security_service = SecurityService()
persistence_service = PersistenceService()

@app.route("/api/v1/cession/calculate", methods=["POST"])
def calculate_cession():
    # 1. Security Validation
    hmac_header = request.headers.get("X-Reinsurance-Hmac")
    if not security_service.validateHmacHeader(hmac_header, request.data):
        return jsonify({"error": "Unauthorized: Invalid X-Reinsurance-Hmac header"}), 401

    # 2. Input Validation
    try:
        data = request.get_json()
        risk_id = data.get("risk_id")
        risk_amount = float(data.get("risk_amount"))
        currency = data.get("currency")

        if not all([risk_id, risk_amount, currency]):
            return jsonify({"error": "Missing required parameters: risk_id, risk_amount, currency"}), 400
        if not isinstance(risk_id, str) or not isinstance(risk_amount, (int, float)) or not isinstance(currency, str):
            return jsonify({"error": "Invalid parameter types"}), 400
        if risk_amount < 0:
            return jsonify({"error": "risk_amount cannot be negative"}), 400

    except Exception as e:
        return jsonify({"error": f"Invalid JSON payload or data types: {e}"}), 400

    # 3. Calculate Cession
    cession_results = cession_calculation_service.calculateCession(risk_id, risk_amount, currency)

    # 4. Persist Results (Mocked for now)
    # The HLD specifies `cessionAmounts` and `reinsurerDetails` as separate dicts for persistence.
    # Adjusting the call to match the HLD's `persistCalculationResult` signature.
    cession_amounts_for_persistence = {
        "retention": cession_results["retention"],
        "reinsurer_a_cession": cession_results["reinsurer_a_cession"],
        "global_re_group_cession": cession_results["global_re_group_cession"]
    }
    reinsurer_details_for_persistence = {
        "Reinsurer A": {"cession_amount": cession_results["reinsurer_a_cession"]},
        "Global Re Group": {"cession_amount": cession_results["global_re_group_cession"]}
    }
    persistence_service.persistCalculationResult(
        risk_id, risk_amount, currency,
        cession_amounts_for_persistence,
        reinsurer_details_for_persistence
    )

    # 5. Return Response
    return jsonify(cession_results), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)