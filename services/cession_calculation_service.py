from typing import Dict
from strategies.retention_strategy import RetentionStrategy
from strategies.proportional_strategy import ProportionalStrategy
from strategies.xol_strategy import XOLStrategy

class CessionCalculationService:
    def __init__(self):
        self.retention_strategy = RetentionStrategy()
        self.proportional_strategy = ProportionalStrategy()
        self.xol_strategy = XOLStrategy()

    def calculateCession(self, risk_id: str, risk_amount: float, currency: str) -> Dict:
        retention = 0.0
        reinsurer_a_cession = 0.0
        global_re_group_cession = 0.0

        # Apply Retention Layer
        if risk_amount <= self.retention_strategy.RETENTION_THRESHOLD:
            retention = risk_amount
        else:
            retention = self.retention_strategy.RETENTION_THRESHOLD
            remaining_risk = risk_amount - retention

            # Apply Proportional Layer
            if remaining_risk > 0 and risk_amount <= self.proportional_strategy.PROPORTIONAL_MAX_THRESHOLD:
                proportional_cession = self.proportional_strategy.calculate_cession(risk_amount)
                reinsurer_a_cession = proportional_cession
                retention += (risk_amount - self.retention_strategy.RETENTION_THRESHOLD) - proportional_cession
            elif risk_amount > self.proportional_strategy.PROPORTIONAL_MAX_THRESHOLD:
                # Calculate proportional cession for the part within the proportional layer
                proportional_cession_base = self.proportional_strategy.PROPORTIONAL_MAX_THRESHOLD - self.retention_strategy.RETENTION_THRESHOLD
                reinsurer_a_cession = proportional_cession_base * self.proportional_strategy.CESSION_PERCENTAGE
                
                # Update retention based on the proportional layer
                retention += proportional_cession_base - reinsurer_a_cession
                
                # Remaining risk after retention and proportional layer
                remaining_risk_after_proportional = risk_amount - self.proportional_strategy.PROPORTIONAL_MAX_THRESHOLD

                # Apply XOL Layer
                if remaining_risk_after_proportional > 0:
                    global_re_group_cession = self.xol_strategy.calculate_cession(risk_amount)
                    # The HLD states "retains the first $50,000,000 and cedes 100% of the surplus"
                    # So, retention should be capped at XOL_THRESHOLD if XOL applies.
                    retention = self.xol_strategy.XOL_THRESHOLD
        
        # Ensure retention is not negative due to floating point inaccuracies or logic errors
        retention = max(0.0, retention)

        return {
            "risk_id": risk_id,
            "risk_amount": risk_amount,
            "currency": currency,
            "retention": retention,
            "reinsurer_a_cession": reinsurer_a_cession,
            "global_re_group_cession": global_re_group_cession
        }