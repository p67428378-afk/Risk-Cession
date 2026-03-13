"""
Module: cession_calculation_service
Purpose: Implements the core logic for calculating risk cession based on defined rules.
Author: Your Name
Created: 2023-10-27
Notes: Uses the Strategy Pattern for reinsurer-specific calculations.
"""

from typing import Dict
from strategies.reinsurer_strategy import ReinsurerStrategy
from strategies.reinsurer_a_strategy import ReinsurerAStrategy
from strategies.global_re_group_strategy import GlobalReGroupStrategy

class CessionCalculationService:
    """
    Service responsible for calculating risk cession based on various layers
    (Retention, Proportional, XOL) and applying reinsurer strategies.
    """
    RETENTION_LAYER_THRESHOLD = 10_000_000.0
    PROPORTIONAL_LAYER_MAX = 50_000_000.0

    def __init__(self):
        self.reinsurer_strategies: Dict[str, ReinsurerStrategy] = {
            "reinsurer_a": ReinsurerAStrategy(),
            "global_re_group": GlobalReGroupStrategy()
        }

    def calculate_cession(self, risk_id: str, risk_amount: float, currency: str) -> Dict:
        """
        Calculates the cession amounts for each reinsurer and the final retention.

        Args:
            risk_id (str): Identifier for the risk.
            risk_amount (float): The total amount of the risk.
            currency (str): The currency of the risk amount.

        Returns:
            dict: A dictionary containing risk details, retention, and cession amounts.
                  Example: {
                      "risk_id": "string",
                      "risk_amount": "number",
                      "currency": "string",
                      "retention": "number",
                      "reinsurer_a_cession": "number",
                      "global_re_group_cession": "number"
                  }
        """
        retention = 0.0
        reinsurer_a_cession = 0.0
        global_re_group_cession = 0.0

        # 1. Retention Layer
        if risk_amount <= self.RETENTION_LAYER_THRESHOLD:
            retention = risk_amount
        else:
            # For risks above retention layer, initial retention is the threshold
            # or the amount remaining after proportional/XOL are considered.
            # The HLD states "retains 100% of the risk" for < $10M, and
            # "retains the first $50,000,000" for XOL.
            # We'll calculate cessions first and then determine final retention.

            # 2. Proportional Layer (Reinsurer A)
            if self.RETENTION_LAYER_THRESHOLD < risk_amount <= self.PROPORTIONAL_LAYER_MAX:
                reinsurer_a_cession, _ = self.reinsurer_strategies["reinsurer_a"].calculate_cession(
                    risk_amount, 0.0 # current_retention is not directly used here for proportional
                )
                retention = risk_amount - reinsurer_a_cession
            elif risk_amount > self.PROPORTIONAL_LAYER_MAX:
                # Reinsurer A's cession is capped at the proportional layer max
                reinsurer_a_cession, _ = self.reinsurer_strategies["reinsurer_a"].calculate_cession(
                    self.PROPORTIONAL_LAYER_MAX, 0.0
                )
                # 3. Excess of Loss (XOL) Layer (Global Re Group)
                global_re_group_cession, _ = self.reinsurer_strategies["global_re_group"].calculate_cession(
                    risk_amount, 0.0 # current_retention is not directly used here for XOL
                )
                # For XOL, the HLD states "retains the first $50,000,000"
                retention = self.PROPORTIONAL_LAYER_MAX - reinsurer_a_cession # Retention up to proportional layer max
                # The remaining amount after XOL cession is also retained up to the XOL threshold
                if risk_amount > self.PROPORTIONAL_LAYER_MAX:
                    retention = self.PROPORTIONAL_LAYER_MAX # Fixed retention for XOL layer

        return {
            "risk_id": risk_id,
            "risk_amount": risk_amount,
            "currency": currency,
            "retention": retention,
            "reinsurer_a_cession": reinsurer_a_cession,
            "global_re_group_cession": global_re_group_cession
        }
