"""
Module: persistence_service
Purpose: Handles the persistence of risk cession calculation results to the database.
Author: Your Name
Created: 2023-10-27
Notes: Uses SQLAlchemy to save CessionResult objects.
"""

from typing import Dict
from sqlalchemy.orm import Session
from models.cession_result import CessionResult

class PersistenceService:
    """
    Service responsible for persisting calculation results to the database.
    """

    def persist_calculation_result(
        self,
        db: Session,
        risk_id: str,
        risk_amount: float,
        currency: str,
        cession_amounts: Dict,
        reinsurer_details: Dict
    ) -> None:
        """
        Persists the risk cession calculation result to the database.

        Args:
            db (Session): The SQLAlchemy database session.
            risk_id (str): The ID of the risk.
            risk_amount (float): The total risk amount.
            currency (str): The currency of the risk.
            cession_amounts (dict): Dictionary containing cession amounts (e.g., retention, reinsurer_a_cession).
            reinsurer_details (dict): Dictionary containing details about reinsurers (not directly used in model, but for future expansion).
        """
        new_cession_result = CessionResult(
            risk_id=risk_id,
            risk_amount=risk_amount,
            currency=currency,
            retention=cession_amounts.get("retention", 0.0),
            reinsurer_a_cession=cession_amounts.get("reinsurer_a_cession", 0.0),
            global_re_group_cession=cession_amounts.get("global_re_group_cession", 0.0)
        )
        db.add(new_cession_result)
        db.commit()
        db.refresh(new_cession_result)
