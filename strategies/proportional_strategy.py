class ProportionalStrategy:
    PROPORTIONAL_MIN_THRESHOLD = 10_000_000.0
    PROPORTIONAL_MAX_THRESHOLD = 50_000_000.0
    CESSION_PERCENTAGE = 0.40  # 40% to Reinsurer A

    def calculate_cession(self, risk_amount: float) -> float:
        if self.PROPORTIONAL_MIN_THRESHOLD < risk_amount <= self.PROPORTIONAL_MAX_THRESHOLD:
            return risk_amount * self.CESSION_PERCENTAGE
        elif risk_amount > self.PROPORTIONAL_MAX_THRESHOLD:
            # For amounts exceeding the proportional layer, calculate cession only on the proportional part
            return (self.PROPORTIONAL_MAX_THRESHOLD - self.PROPORTIONAL_MIN_THRESHOLD) * self.CESSION_PERCENTAGE
        return 0.0