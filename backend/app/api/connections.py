"""
Connections API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc
from typing import Optional
from ..database import get_db
from ..models import Connection
from ..schemas.connection import ConnectionResponse, PaginatedConnectionsResponse

router = APIRouter()


@router.get("/", response_model=PaginatedConnectionsResponse)
def list_connections(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    job_function: Optional[str] = None,
    seniority_level: Optional[str] = None,
    is_ai_ml: Optional[bool] = None,
    is_founder: Optional[bool] = None,
    is_recruiter: Optional[bool] = None,
    is_engineer: Optional[bool] = None,
    is_cxo: Optional[bool] = None,
    company_id: Optional[int] = None,
    min_score: Optional[float] = None,
    max_score: Optional[float] = None,
    search: Optional[str] = None,
    sort_by: str = Query("total_score", regex="^[a-z_]+$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db),
):
    """
    List connections with filtering, searching, sorting, and pagination.

    Args:
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
        job_function: Filter by job function
        seniority_level: Filter by seniority level
        is_ai_ml: Filter by AI/ML flag
        is_founder: Filter by founder flag
        is_recruiter: Filter by recruiter flag
        is_engineer: Filter by engineer flag
        is_cxo: Filter by C-level flag
        company_id: Filter by company ID
        min_score: Minimum total score
        max_score: Maximum total score
        search: Search by name, company, or position
        sort_by: Field to sort by
        sort_order: Sort order (asc or desc)
        db: Database session

    Returns:
        Paginated list of connections
    """
    query = db.query(Connection)

    # Apply filters
    if job_function:
        query = query.filter(Connection.job_function == job_function)

    if seniority_level:
        query = query.filter(Connection.seniority_level == seniority_level)

    if is_ai_ml is not None:
        query = query.filter(Connection.is_ai_ml == is_ai_ml)

    if is_founder is not None:
        query = query.filter(Connection.is_founder == is_founder)

    if is_recruiter is not None:
        query = query.filter(Connection.is_recruiter == is_recruiter)

    if is_engineer is not None:
        query = query.filter(Connection.is_engineer == is_engineer)

    if is_cxo is not None:
        query = query.filter(Connection.is_cxo == is_cxo)

    if company_id:
        query = query.filter(Connection.company_id == company_id)

    if min_score is not None:
        query = query.filter(Connection.total_score >= min_score)

    if max_score is not None:
        query = query.filter(Connection.total_score <= max_score)

    # Search by name, company, or position
    if search:
        search_filter = or_(
            Connection.full_name_normalized.ilike(f"%{search}%"),
            Connection.company_normalized.ilike(f"%{search}%"),
            Connection.position_normalized.ilike(f"%{search}%"),
        )
        query = query.filter(search_filter)

    # Count total before pagination
    total = query.count()

    # Sorting
    if hasattr(Connection, sort_by):
        sort_column = getattr(Connection, sort_by)
        if sort_order == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))

    # Pagination
    connections = query.offset(skip).limit(limit).all()

    return {
        "items": connections,
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.get("/{connection_id}", response_model=ConnectionResponse)
def get_connection(connection_id: int, db: Session = Depends(get_db)):
    """
    Get a single connection by ID.

    Args:
        connection_id: Connection ID
        db: Database session

    Returns:
        Connection details
    """
    connection = db.query(Connection).filter(Connection.id == connection_id).first()

    if not connection:
        raise HTTPException(status_code=404, detail="Connection not found")

    return connection


@router.delete("/{connection_id}")
def delete_connection(connection_id: int, db: Session = Depends(get_db)):
    """
    Delete a connection.

    Args:
        connection_id: Connection ID
        db: Database session

    Returns:
        Success message
    """
    connection = db.query(Connection).filter(Connection.id == connection_id).first()

    if not connection:
        raise HTTPException(status_code=404, detail="Connection not found")

    db.delete(connection)
    db.commit()

    return {"message": "Connection deleted successfully"}
