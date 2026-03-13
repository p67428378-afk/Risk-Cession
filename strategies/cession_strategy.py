from abc import ABC, abstractmethod

class CessionStrategy(ABC):
    """
    Abstract base class for cession strategies.
    Each concrete strategy will implement the calculate_cession method
    based on specific reinsurance rules.
    """
    @abstractmethod
    def calculate_cession(self, risk_amount: float) -> float:
        """
        Calculates the cession amount for a specific reinsurance layer.

        Args:
            risk_amount (float): The total risk amount.

        Returns:
            float: The calculated cession amount for this strategy.
        """
        pass