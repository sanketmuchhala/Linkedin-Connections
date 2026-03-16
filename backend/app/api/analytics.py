"""
Analytics API endpoints.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from ..database import get_db
from ..models import Connection, Company
from ..schemas.analytics import OverviewAnalytics

router = APIRouter()


@router.get("/overview", response_model=OverviewAnalytics)
def get_overview_analytics(db: Session = Depends(get_db)):
    """
    Get overview dashboard analytics.

    Returns:
        Overview statistics and charts data
    """
    # Basic counts
    total_connections = db.query(Connection).count()
    total_companies = db.query(Company).count()

    # Flag counts
    ai_ml_count = db.query(Connection).filter(Connection.is_ai_ml == True).count()
    founder_count = db.query(Connection).filter(Connection.is_founder == True).count()
    recruiter_count = db.query(Connection).filter(Connection.is_recruiter == True).count()

    # Top companies by network strength
    top_companies_query = (
        db.query(Company)
        .order_by(Company.network_strength.desc())
        .limit(10)
        .all()
    )

    top_companies = [
        {
            "name": company.name_normalized,
            "total_connections": company.total_connections,
            "network_strength": company.network_strength,
            "ai_ml_count": company.ai_ml_count,
        }
        for company in top_companies_query
    ]

    # Connection growth over time (by month)
    connection_growth_query = (
        db.query(
            extract('year', Connection.connected_on).label('year'),
            extract('month', Connection.connected_on).label('month'),
            func.count(Connection.id).label('count'),
        )
        .group_by('year', 'month')
        .order_by('year', 'month')
        .all()
    )

    connection_growth = [
        {
            "month": f"{int(row.year)}-{int(row.month):02d}",
            "count": row.count,
        }
        for row in connection_growth_query
    ]

    # Seniority distribution
    seniority_dist_query = (
        db.query(
            Connection.seniority_level,
            func.count(Connection.id).label('count'),
        )
        .filter(Connection.seniority_level.isnot(None))
        .group_by(Connection.seniority_level)
        .all()
    )

    seniority_distribution = [
        {
            "seniority": row.seniority_level,
            "count": row.count,
        }
        for row in seniority_dist_query
    ]

    return {
        "total_connections": total_connections,
        "total_companies": total_companies,
        "ai_ml_count": ai_ml_count,
        "founder_count": founder_count,
        "recruiter_count": recruiter_count,
        "top_companies": top_companies,
        "connection_growth": connection_growth,
        "seniority_distribution": seniority_distribution,
    }
