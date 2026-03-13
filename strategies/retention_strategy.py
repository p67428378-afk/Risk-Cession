class RetentionStrategy:
    RETENTION_THRESHOLD = 10_000_000.0

    def calculate_cession(self, risk_amount: float) -> float:
        if risk_amount <= self.RETENTION_THRESHOLD:
            return risk_amount  # Fully retained
        return self.RETENTION_THRESHOLD # Retain up to the threshold