"""
Companies API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from typing import Optional
from ..database import get_db
from ..models import Company
from ..schemas.company import CompanyResponse, PaginatedCompaniesResponse

router = APIRouter()


@router.get("/", response_model=PaginatedCompaniesResponse)
def list_companies(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    min_connections: Optional[int] = None,
    min_network_strength: Optional[float] = None,
    search: Optional[str] = None,
    sort_by: str = Query("network_strength", regex="^[a-z_]+$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db),
):
    """
    List companies with filtering, searching, and sorting.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        min_connections: Minimum number of connections
        min_network_strength: Minimum network strength score
        search: Search by company name
        sort_by: Field to sort by
        sort_order: Sort order (asc or desc)
        db: Database session

    Returns:
        Paginated list of companies
    """
    query = db.query(Company)

    # Apply filters
    if min_connections:
        query = query.filter(Company.total_connections >= min_connections)

    if min_network_strength:
        query = query.filter(Company.network_strength >= min_network_strength)

    if search:
        query = query.filter(Company.name_normalized.ilike(f"%{search}%"))

    # Count total
    total = query.count()

    # Sorting
    if hasattr(Company, sort_by):
        sort_column = getattr(Company, sort_by)
        if sort_order == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))

    # Pagination
    companies = query.offset(skip).limit(limit).all()

    return {
        "items": companies,
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(company_id: int, db: Session = Depends(get_db)):
    """
    Get a single company by ID.

    Args:
        company_id: Company ID
        db: Database session

    Returns:
        Company details
    """
    company = db.query(Company).filter(Company.id == company_id).first()

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    return company
