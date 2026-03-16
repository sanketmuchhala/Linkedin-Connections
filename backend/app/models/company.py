"""
Company model for aggregating connection data by company.
"""
from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class Company(Base):
    """Model for storing aggregated company metrics."""

    __tablename__ = "companies"

    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Company Data
    name = Column(String, nullable=False)
    name_normalized = Column(String, unique=True, nullable=False, index=True)

    # Aggregated Metrics
    total_connections = Column(Integer, default=0)
    engineer_count = Column(Integer, default=0)
    recruiter_count = Column(Integer, default=0)
    founder_count = Column(Integer, default=0)
    ai_ml_count = Column(Integer, default=0)
    cxo_count = Column(Integer, default=0)

    # Average Scores
    avg_outreach_score = Column(Float, default=0.0)
    avg_relevance_score = Column(Float, default=0.0)
    avg_influence_score = Column(Float, default=0.0)

    # Network Strength (0-100)
    network_strength = Column(Float, default=0.0, index=True)

    # Top Seniority Level (highest level in this company)
    top_seniority = Column(String, nullable=True)

    # Company Type
    company_type = Column(String, nullable=True)  # startup, big_tech, enterprise, university

    # Metadata
    first_connection_date = Column(Date, nullable=True)
    last_connection_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    connections = relationship("Connection", back_populates="company")

    def __repr__(self):
        return f"<Company(id={self.id}, name={self.name_normalized}, connections={self.total_connections}, network_strength={self.network_strength})>"
