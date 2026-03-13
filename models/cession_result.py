"""
Module: cession_result
Purpose: Defines the SQLAlchemy model for storing risk cession calculation results.
Author: Your Name
Created: 2023-10-27
Notes: Corresponds to the HLD's response schema for persistence.
"""

from sqlalchemy import Column, String, Float, Integer
from database import Base

class CessionResult(Base):
    """
    SQLAlchemy model for storing risk cession calculation results.
    """
    __tablename__ = "cession_results"

    id = Column(Integer, primary_key=True, index=True)
    risk_id = Column(String, index=True, nullable=False)
    risk_amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    retention = Column(Float, nullable=False)
    reinsurer_a_cession = Column(Float, nullable=False)
    global_re_group_cession = Column(Float, nullable=False)

    def __repr__(self):
        return (f"<CessionResult(risk_id='{self.risk_id}', risk_amount={self.risk_amount}, "
                f"retention={self.retention}, reinsurer_a_cession={self.reinsurer_a_cession}, "
                f"global_re_group_cession={self.global_re_group_cession})>")
