from typing import Dict
from models.cession_result import CessionResult, Session, engine, Base
import uuid

class PersistenceService:
    """
    Service responsible for persisting the calculation result to the database.
    """
    def __init__(self):
        # Ensure tables are created if they don't exist
        Base.metadata.create_all(engine)

    def persistCalculationResult(self,
                                 risk_id: str,
                                 risk_amount: float,
                                 currency: str,
                                 cession_amounts: Dict) -> None:
        """
        Persists the risk cession calculation result to the database.

        Args:
            risk_id (str): The unique identifier for the risk.
            risk_amount (float): The total amount of the risk.
            currency (str): The currency of the risk amount.
            cession_amounts (Dict): A dictionary containing retention and reinsurer cession amounts.
                                    Expected keys: 'retention', 'reinsurer_a_cession', 'global_re_group_cession'.
        """
        session = Session()
        try:
            new_cession_result = CessionResult(
                id=str(uuid.uuid4()), # Generate a unique ID for the record
                risk_id=risk_id,
                risk_amount=risk_amount,
                currency=currency,
                retention=cession_amounts.get("retention", 0.0),
                reinsurer_a_cession=cession_amounts.get("reinsurer_a_cession", 0.0),
                global_re_group_cession=cession_amounts.get("global_re_group_cession", 0.0)
            )
            session.add(new_cession_result)
            session.commit()
            print(f"Successfully persisted cession result for risk_id: {risk_id}")
        except Exception as e:
            session.rollback()
            print(f"Error persisting cession result for risk_id {risk_id}: {e}")
            raise # Re-raise the exception after logging and rolling back
        finally:
            session.close()