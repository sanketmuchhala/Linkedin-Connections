"""
Pydantic schemas for Analytics API endpoints.
"""
from pydantic import BaseModel
from typing import List, Dict


class OverviewAnalytics(BaseModel):
    """Overview dashboard analytics."""
    total_connections: int
    total_companies: int
    ai_ml_count: int
    founder_count: int
    recruiter_count: int
    top_companies: List[Dict]
    connection_growth: List[Dict]
    seniority_distribution: List[Dict]
