class PersistenceService:
    def __init__(self):
        self.db = []  # In-memory list to simulate database persistence

    def persistCalculationResult(self, risk_id: str, risk_amount: float, currency: str, cession_amounts: dict, reinsurer_details: dict) -> None:
        record = {
            "risk_id": risk_id,
            "risk_amount": risk_amount,
            "currency": currency,
            "cession_amounts": cession_amounts,
            "reinsurer_details": reinsurer_details
        }
        self.db.append(record)
        print(f"Persisted: {record}") # For demonstration
