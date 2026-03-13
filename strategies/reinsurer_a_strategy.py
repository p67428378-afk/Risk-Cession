from .cession_strategy import CessionStrategy

class ReinsurerAStrategy(CessionStrategy):
    """
    Implements the proportional layer cession strategy for 'Reinsurer A'.
    Cedes 40% of the risk for amounts between $10,000,000 and $50,000,000.
    """
    def calculate_cession(self, risk_amount: float) -> float:
        """
        Calculates the cession amount for Reinsurer A.

        Args:
            risk_amount (float): The total risk amount.

        Returns:
            float: The calculated cession amount for Reinsurer A.
        """
        if 10_000_000 < risk_amount <= 50_000_000:
            return risk_amount * 0.40
        return 0.0