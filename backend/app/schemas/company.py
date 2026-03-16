"""
Pydantic schemas for Company API endpoints.
"""
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class CompanyResponse(BaseModel):
    """Company response schema."""
    id: int
    name_normalized: str
    total_connections: int = 0
    engineer_count: int = 0
    recruiter_count: int = 0
    founder_count: int = 0
    ai_ml_count: int = 0
    cxo_count: int = 0
    avg_outreach_score: float = 0.0
    network_strength: float = 0.0
    top_seniority: Optional[str] = None
    company_type: Optional[str] = None
    first_connection_date: Optional[date] = None
    last_connection_date: Optional[date] = None

    class Config:
        from_attributes = True


class PaginatedCompaniesResponse(BaseModel):
    """Paginated companies response."""
    items: list[CompanyResponse]
    total: int
    skip: int
    limit: int
