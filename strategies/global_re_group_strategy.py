from .cession_strategy import CessionStrategy

class GlobalReGroupStrategy(CessionStrategy):
    """
    Implements the Excess of Loss (XOL) layer cession strategy for 'Global Re Group'.
    Cedes 100% of the surplus exceeding $50,000,000, up to a maximum limit of $200,000,000.
    """
    def calculate_cession(self, risk_amount: float) -> float:
        """
        Calculates the cession amount for Global Re Group (XOL layer).

        Args:
            risk_amount (float): The total risk amount.

        Returns:
            float: The calculated cession amount for Global Re Group.
        """
        if risk_amount > 50_000_000:
            surplus = risk_amount - 50_000_000
            # Cede 100% of the surplus, up to a maximum of $200,000,000
            return min(surplus, 200_000_000)
        return 0.0