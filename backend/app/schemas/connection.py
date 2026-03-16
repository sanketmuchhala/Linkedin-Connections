"""
Pydantic schemas for Connection API endpoints.
"""
from pydantic import BaseModel
from typing import Optional, Dict
from datetime import date, datetime


class ConnectionBase(BaseModel):
    """Base connection schema."""
    first_name_normalized: str
    last_name_normalized: str
    full_name_normalized: str
    company_normalized: Optional[str] = None
    position_normalized: Optional[str] = None


class ConnectionResponse(BaseModel):
    """Connection response schema."""
    id: int
    first_name_normalized: str
    last_name_normalized: str
    full_name_normalized: str
    linkedin_url: str
    email_address: Optional[str] = None
    company_normalized: Optional[str] = None
    position_normalized: Optional[str] = None
    connected_on: Optional[date] = None

    job_function: Optional[str] = None
    seniority_level: Optional[str] = None

    is_recruiter: bool = False
    is_founder: bool = False
    is_cxo: bool = False
    is_ai_ml: bool = False
    is_engineer: bool = False
    is_student: bool = False
    is_researcher: bool = False

    outreach_score: float = 0.0
    relevance_score: float = 0.0
    influence_score: float = 0.0
    total_score: float = 0.0
    score_breakdown: Optional[Dict] = None

    outreach_status: Optional[str] = None

    company_id: Optional[int] = None

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PaginatedConnectionsResponse(BaseModel):
    """Paginated connections response."""
    items: list[ConnectionResponse]
    total: int
    skip: int
    limit: int
