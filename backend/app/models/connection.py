"""
Connection model representing LinkedIn connections.
"""
from sqlalchemy import Column, Integer, String, Boolean, Float, Date, DateTime, ForeignKey, JSON, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base
from ..core.enums import JobFunction, SeniorityLevel


class Connection(Base):
    """Model for storing LinkedIn connection data."""

    __tablename__ = "connections"

    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Raw Data (from CSV)
    first_name_raw = Column(String, nullable=False)
    last_name_raw = Column(String, nullable=False)
    linkedin_url = Column(String, unique=True, nullable=False, index=True)
    email_address = Column(String, nullable=True, index=True)
    company_raw = Column(String, nullable=True)
    position_raw = Column(String, nullable=True)
    connected_on = Column(Date, nullable=False, index=True)

    # Normalized Data
    first_name_normalized = Column(String, nullable=False, index=True)
    last_name_normalized = Column(String, nullable=False, index=True)
    full_name_normalized = Column(String, nullable=False, index=True)
    company_normalized = Column(String, nullable=True, index=True)
    position_normalized = Column(String, nullable=True, index=True)

    # Classification Fields
    job_function = Column(String, nullable=True, index=True)  # JobFunction enum
    seniority_level = Column(String, nullable=True, index=True)  # SeniorityLevel enum

    # Classification Flags (Boolean indexes)
    is_recruiter = Column(Boolean, default=False, index=True)
    is_founder = Column(Boolean, default=False, index=True)
    is_cxo = Column(Boolean, default=False, index=True)
    is_ai_ml = Column(Boolean, default=False, index=True)
    is_engineer = Column(Boolean, default=False, index=True)
    is_student = Column(Boolean, default=False, index=True)
    is_researcher = Column(Boolean, default=False, index=True)

    # Scores (0-100 scale)
    outreach_score = Column(Float, default=0.0, index=True)
    relevance_score = Column(Float, default=0.0, index=True)
    influence_score = Column(Float, default=0.0, index=True)
    total_score = Column(Float, default=0.0, index=True)

    # Score Explanation (JSON)
    score_breakdown = Column(JSON, nullable=True)

    # Outreach Status
    outreach_status = Column(String, nullable=True, index=True)  # not_contacted, queued, messaged, replied, etc.

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_processed_at = Column(DateTime, nullable=True)

    # Foreign Keys
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True, index=True)

    # Relationships
    company = relationship("Company", back_populates="connections")
    outreach_logs = relationship("OutreachLog", back_populates="connection", cascade="all, delete-orphan")

    # Composite Indexes for common queries
    __table_args__ = (
        Index('idx_score_composite', 'total_score', 'is_ai_ml', 'is_founder'),
        Index('idx_classification', 'job_function', 'seniority_level'),
        Index('idx_company_function', 'company_id', 'job_function'),
    )

    def __repr__(self):
        return f"<Connection(id={self.id}, name={self.full_name_normalized}, score={self.total_score})>"
