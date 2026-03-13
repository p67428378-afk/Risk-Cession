"""
Module: global_re_group_strategy
Purpose: Implements the cession calculation strategy for Global Re Group.
Author: Your Name
Created: 2023-10-27
Notes: Handles the Excess of Loss (XOL) layer as per HLD.
"""

from strategies.reinsurer_strategy import ReinsurerStrategy

class GlobalReGroupStrategy(ReinsurerStrategy):
    """
    Strategy for calculating cession for 'Global Re Group' based on the XOL layer.
    - For risks exceeding $50,000,000, cedes 100% of the surplus to 'Global Re Group',
      up to a maximum limit of $200,000,000.
    """
    XOL_LAYER_THRESHOLD = 50_000_000.0
    XOL_CESSION_LIMIT = 200_000_000.0

    def calculate_cession(self, risk_amount: float, current_retention: float) -> tuple[float, float]:
        """
        Calculates the cession amount for Global Re Group.

        Args:
            risk_amount (float): The total risk amount.
            current_retention (float): The amount currently retained by the insurer.

        Returns:
            tuple[float, float]: A tuple containing (cession_amount, updated_retention).
        """
        cession_amount = 0.0
        updated_retention = current_retention # XOL cession doesn't directly reduce current_retention in this model

        if risk_amount > self.XOL_LAYER_THRESHOLD:
            surplus = risk_amount - self.XOL_LAYER_THRESHOLD
            cession_amount = min(surplus, self.XOL_CESSION_LIMIT)
            # The HLD states "the service retains the first $50,000,000" for XOL.
            # This means the retention for the XOL layer is fixed at $50M if risk_amount > XOL_LAYER_THRESHOLD.
            # The main CessionCalculationService will manage the overall retention.
            # This strategy only calculates Global Re Group's specific cession.

        return cession_amount, updated_retention
