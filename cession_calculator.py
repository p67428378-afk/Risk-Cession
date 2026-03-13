from abc import ABC, abstractmethod

class ReinsurerStrategy(ABC):
    @abstractmethod
    def calculate_cession(self, risk_amount: float) -> float:
        pass

class RetentionStrategy(ReinsurerStrategy):
    def calculate_cession(self, risk_amount: float) -> float:
        if risk_amount <= 10_000_000:
            return risk_amount  # Retain 100%
        return 0.0

class ProportionalStrategy(ReinsurerStrategy):
    def calculate_cession(self, risk_amount: float) -> float:
        if 10_000_000 < risk_amount <= 50_000_000:
            return risk_amount * 0.40  # Cede 40% to Reinsurer A
        return 0.0

class XOLStrategy(ReinsurerStrategy):
    def calculate_cession(self, risk_amount: float) -> float:
        if risk_amount > 50_000_000:
            excess_amount = risk_amount - 50_000_000
            # Cede 100% of surplus up to a maximum limit of $200,000,000
            return min(excess_amount, 200_000_000.0)
        return 0.0

class CessionCalculationService:
    def __init__(self):
        self.strategies = {
            "retention": RetentionStrategy(),
            "reinsurer_a": ProportionalStrategy(),
            "global_re_group": XOLStrategy()
        }

    def calculateCession(self, risk_id: str, risk_amount: float, currency: str) -> dict:
        retention_amount = self.strategies["retention"].calculate_cession(risk_amount)
        reinsurer_a_cession = self.strategies["reinsurer_a"].calculate_cession(risk_amount)
        global_re_group_cession = self.strategies["global_re_group"].calculate_cession(risk_amount)

        # Adjust retention if proportional or XOL cession occurs
        if reinsurer_a_cession > 0:
            retention_amount = risk_amount - reinsurer_a_cession
        elif global_re_group_cession > 0:
            retention_amount = 50_000_000.0 # Retain first 50M for XOL
        elif retention_amount == 0 and risk_amount <= 10_000_000:
            retention_amount = risk_amount # Ensure full retention for small risks

        return {
            "risk_id": risk_id,
            "risk_amount": risk_amount,
            "currency": currency,
            "retention": retention_amount,
            "reinsurer_a_cession": reinsurer_a_cession,
            "global_re_group_cession": global_re_group_cession
        }
