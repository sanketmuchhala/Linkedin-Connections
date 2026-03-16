"""
Outreach Log model for tracking outreach activities (mini CRM).
"""
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class OutreachLog(Base):
    """Model for tracking outreach activities."""

    __tablename__ = "outreach_logs"

    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Foreign Key
    connection_id = Column(Integer, ForeignKey("connections.id"), nullable=False, index=True)

    # Outreach Data
    outreach_type = Column(String, nullable=False)  # OutreachType enum: message, email, meeting, call, referral
    status = Column(String, nullable=False, index=True)  # OutreachStatus enum: planned, sent, replied, etc.

    subject = Column(String, nullable=True)
    notes = Column(Text, nullable=True)

    # Dates
    planned_date = Column(Date, nullable=True)
    completed_date = Column(Date, nullable=True)
    follow_up_date = Column(Date, nullable=True, index=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    connection = relationship("Connection", back_populates="outreach_logs")

    def __repr__(self):
        return f"<OutreachLog(id={self.id}, connection_id={self.connection_id}, type={self.outreach_type}, status={self.status})>"
