from datetime import datetime
from sqlalchemy import create_engine, Column, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from config import Config

Base = declarative_base()

class CessionResult(Base):
    __tablename__ = 'cession_results'

    id = Column(String, primary_key=True)
    risk_id = Column(String, nullable=False)
    risk_amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    retention = Column(Float, nullable=False)
    reinsurer_a_cession = Column(Float, nullable=False)
    global_re_group_cession = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<CessionResult(risk_id='{self.risk_id}', risk_amount={self.risk_amount}, retention={self.retention})>"

# Setup for database connection (can be used for migrations or direct script interaction)
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)