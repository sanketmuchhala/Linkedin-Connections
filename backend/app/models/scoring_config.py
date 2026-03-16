"""
Scoring Configuration model for managing scoring weights.
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON
from datetime import datetime
from ..database import Base


class ScoringConfig(Base):
    """Model for storing scoring configuration."""

    __tablename__ = "scoring_configs"

    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Config Metadata
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=False, index=True)
    # Only one config can be active at a time

    # Weights (JSON for flexibility)
    weights = Column(JSON, nullable=False)
    # Structure:
    # {
    #   "base_weights": {
    #     "seniority": 0.30,
    #     "function": 0.25,
    #     "recency": 0.20,
    #     "company": 0.15,
    #     "email": 0.10
    #   },
    #   "seniority_scores": {
    #     "intern": 10, "junior": 20, "mid": 40, "senior": 60,
    #     "lead": 70, "manager": 75, "director": 85, "vp": 90,
    #     "c_level": 95, "founder": 100
    #   },
    #   "function_scores": {
    #     "data_science": 85, "engineering": 80, "executive": 90,
    #     "product": 70, "design": 60, "sales": 40, "marketing": 40,
    #     "hr": 30, "other": 50
    #   },
    #   "flag_bonuses": {
    #     "is_ai_ml": 15,
    #     "is_founder": 20,
    #     "is_cxo": 15,
    #     "is_recruiter": -10,
    #     "is_engineer_and_ai_ml": 5,
    #     "dense_company": 5
    #   }
    # }

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<ScoringConfig(id={self.id}, name={self.name}, is_active={self.is_active})>"
