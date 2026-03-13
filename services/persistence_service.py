from typing import Dict, List
from models.cession_result import CessionResult

class PersistenceService:
    _in_memory_db: List[CessionResult] = [] # Simple in-memory list as a mock database

    def persistCalculationResult(self, risk_id: str, risk_amount: float, currency: str, cession_amounts: Dict, reinsurer_details: Dict) -> None:
        # In a real application, this would interact with a database (e.g., PostgreSQL)
        # For this exercise, we'll store it in a simple in-memory list.
        print(f"Persisting calculation result for risk_id: {risk_id}")
        result = CessionResult(
            risk_id=risk_id,
            risk_amount=risk_amount,
            currency=currency,
            retention=cession_amounts.get("retention", 0.0),
            reinsurer_a_cession=cession_amounts.get("reinsurer_a_cession", 0.0),
            global_re_group_cession=cession_amounts.get("global_re_group_cession", 0.0)
        )
        self._in_memory_db.append(result)
        print(f"Current in-memory DB size: {len(self._in_memory_db)}")