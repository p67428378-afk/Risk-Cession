"""
Module: reinsurer_strategy
Purpose: Defines the abstract base class for reinsurer strategies.
Author: Your Name
Created: 2023-10-27
Notes: Part of the Strategy Pattern implementation.
"""

from abc import ABC, abstractmethod

class ReinsurerStrategy(ABC):
    """
    Abstract base class for all reinsurer strategies.
    Defines the interface for calculating cession amounts for a specific reinsurer.
    """

    @abstractmethod
    def calculate_cession(self, risk_amount: float, current_retention: float) -> tuple[float, float]:
        """
        Calculates the cession amount for a specific reinsurer and updates retention.

        Args:
            risk_amount (float): The total risk amount.
            current_retention (float): The amount currently retained by the insurer.

        Returns:
            tuple[float, float]: A tuple containing (cession_amount, updated_retention).
        """
        pass
