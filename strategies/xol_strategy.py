class XOLStrategy:
    XOL_THRESHOLD = 50_000_000.0
    XOL_MAX_CESSION = 200_000_000.0

    def calculate_cession(self, risk_amount: float) -> float:
        if risk_amount > self.XOL_THRESHOLD:
            surplus = risk_amount - self.XOL_THRESHOLD
            return min(surplus, self.XOL_MAX_CESSION)
        return 0.0