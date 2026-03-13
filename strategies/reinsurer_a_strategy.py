"""
Module: reinsurer_a_strategy
Purpose: Implements the cession calculation strategy for Reinsurer A.
Author: Your Name
Created: 2023-10-27
Notes: Handles the proportional layer as per HLD.
"""

from strategies.reinsurer_strategy import ReinsurerStrategy

class ReinsurerAStrategy(ReinsurerStrategy):
    """
    Strategy for calculating cession for 'Reinsurer A' based on the proportional layer.
    - For risks between $10,000,000 and $50,000,000, cedes 40% of the risk to 'Reinsurer A'.
    """
    PROPORTIONAL_LAYER_MIN = 10_000_000.0
    PROPORTIONAL_LAYER_MAX = 50_000_000.0
    CESSION_PERCENTAGE = 0.40

    def calculate_cession(self, risk_amount: float, current_retention: float) -> tuple[float, float]:
        """
        Calculates the cession amount for Reinsurer A.

        Args:
            risk_amount (float): The total risk amount.
            current_retention (float): The amount currently retained by the insurer.

        Returns:
            tuple[float, float]: A tuple containing (cession_amount, updated_retention).
        """
        cession_amount = 0.0
        updated_retention = current_retention

        if self.PROPORTIONAL_LAYER_MIN <= risk_amount <= self.PROPORTIONAL_LAYER_MAX:
            cession_amount = risk_amount * self.CESSION_PERCENTAGE
            updated_retention = risk_amount - cession_amount
        elif risk_amount > self.PROPORTIONAL_LAYER_MAX:
            # For risks exceeding the proportional layer, Reinsurer A's cession is based
            # on the proportional layer's maximum amount.
            # This assumes Reinsurer A only participates up to the proportional layer max.
            # The HLD states "For risks between $10,000,000 and $50,000,000, the service cedes 40% of the risk to 'Reinsurer A'."
            # This implies Reinsurer A's participation is capped at the proportional layer max.
            cession_amount = self.PROPORTIONAL_LAYER_MAX * self.CESSION_PERCENTAGE
            # Retention is handled by the main calculation logic, this strategy only calculates its cession.

        return cession_amount, updated_retention
