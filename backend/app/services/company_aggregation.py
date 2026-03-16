"""
Company aggregation service for calculating company-level metrics.
"""
from sqlalchemy.orm import Session
from typing import List, Optional
import numpy as np


class CompanyAggregationService:
    """Aggregate company-level metrics from connections."""

    # Seniority level rankings for comparison
    SENIORITY_RANKS = {
        "intern": 1,
        "junior": 2,
        "mid": 3,
        "senior": 4,
        "lead": 5,
        "manager": 6,
        "director": 7,
        "vp": 8,
        "c_level": 9,
        "founder": 10,
    }

    def __init__(self, db: Session):
        """
        Initialize with database session.

        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    def recalculate_all_companies(self):
        """Recalculate metrics for all companies."""
        from ..models import Company

        companies = self.db.query(Company).all()

        for company in companies:
            self.recalculate_company(company)

        self.db.commit()

    def recalculate_company(self, company):
        """
        Recalculate metrics for a single company.

        Args:
            company: Company model instance
        """
        connections = company.connections

        if not connections:
            # Reset to defaults if no connections
            company.total_connections = 0
            company.engineer_count = 0
            company.recruiter_count = 0
            company.founder_count = 0
            company.ai_ml_count = 0
            company.cxo_count = 0
            company.avg_outreach_score = 0.0
            company.avg_relevance_score = 0.0
            company.avg_influence_score = 0.0
            company.network_strength = 0.0
            company.top_seniority = None
            company.first_connection_date = None
            company.last_connection_date = None
            return

        # Basic counts
        company.total_connections = len(connections)
        company.engineer_count = sum(1 for c in connections if c.is_engineer)
        company.recruiter_count = sum(1 for c in connections if c.is_recruiter)
        company.founder_count = sum(1 for c in connections if c.is_founder)
        company.ai_ml_count = sum(1 for c in connections if c.is_ai_ml)
        company.cxo_count = sum(1 for c in connections if c.is_cxo)

        # Average scores
        scores = [c.outreach_score for c in connections if c.outreach_score is not None]
        company.avg_outreach_score = float(np.mean(scores)) if scores else 0.0

        relevance_scores = [c.relevance_score for c in connections if c.relevance_score is not None]
        company.avg_relevance_score = float(np.mean(relevance_scores)) if relevance_scores else 0.0

        influence_scores = [c.influence_score for c in connections if c.influence_score is not None]
        company.avg_influence_score = float(np.mean(influence_scores)) if influence_scores else 0.0

        # Network strength calculation
        company.network_strength = self.calculate_network_strength(connections)

        # Top seniority level
        company.top_seniority = self.get_top_seniority(connections)

        # Date range
        connection_dates = [c.connected_on for c in connections if c.connected_on]
        if connection_dates:
            company.first_connection_date = min(connection_dates)
            company.last_connection_date = max(connection_dates)

        # Infer company type if not set
        if not company.company_type:
            company.company_type = self.infer_company_type(company, connections)

    def calculate_network_strength(self, connections: List) -> float:
        """
        Calculate network strength score based on quality and diversity.

        Formula:
        - Quality (70%): Average of top 10% connection scores
        - Diversity (30%): Ratio of unique job functions represented

        Args:
            connections: List of Connection model instances

        Returns:
            Network strength score (0-100)
        """
        if not connections:
            return 0.0

        # Quality: average of top 10% scores (or all if fewer than 10)
        scores = [c.total_score for c in connections if c.total_score is not None]
        if not scores:
            quality_score = 0.0
        else:
            scores_sorted = sorted(scores, reverse=True)
            top_n = max(1, len(scores_sorted) // 10)
            quality_score = float(np.mean(scores_sorted[:top_n]))

        # Diversity: unique job functions represented
        # There are 12 possible job functions (including "other")
        unique_functions = len(set(c.job_function for c in connections if c.job_function))
        diversity_score = min(unique_functions / 12 * 100, 100)

        # Combine (weighted)
        network_strength = quality_score * 0.7 + diversity_score * 0.3

        return round(network_strength, 1)

    def get_top_seniority(self, connections: List) -> Optional[str]:
        """
        Get the highest seniority level among connections.

        Args:
            connections: List of Connection model instances

        Returns:
            Top seniority level (SeniorityLevel enum value) or None
        """
        seniority_levels = [c.seniority_level for c in connections if c.seniority_level]

        if not seniority_levels:
            return None

        # Find the highest seniority using ranks
        top_seniority = max(
            seniority_levels,
            key=lambda s: self.SENIORITY_RANKS.get(s, 0)
        )

        return top_seniority

    def infer_company_type(self, company, connections: List) -> str:
        """
        Infer company type based on company name and connections.

        Args:
            company: Company model instance
            connections: List of Connection model instances

        Returns:
            Company type (CompanyType enum value)
        """
        company_name = company.name_normalized.lower()

        # University
        if any(word in company_name for word in ["university", "college", "institute", "school"]):
            return "university"

        # Startup indicators
        if "stealth" in company_name:
            return "startup"

        # Check if has multiple founders (strong startup indicator)
        if company.founder_count >= 2:
            return "startup"

        # Big tech (known companies)
        big_tech_names = [
            "google", "microsoft", "amazon", "meta", "apple", "netflix",
            "facebook", "alphabet", "tesla", "nvidia", "intel", "ibm",
            "oracle", "salesforce", "adobe", "vmware"
        ]
        if any(company_name == tech or company_name.startswith(tech + " ") for tech in big_tech_names):
            return "big_tech"

        # Enterprise (large companies with many connections, high diversity)
        if company.total_connections > 20 and company.network_strength > 50:
            return "enterprise"

        # Default
        return "unknown"

    def create_or_update_company(self, normalized_company_name: str) -> 'Company':
        """
        Create a new company or get existing one by normalized name.

        Args:
            normalized_company_name: Normalized company name

        Returns:
            Company model instance
        """
        from ..models import Company

        if not normalized_company_name:
            return None

        # Check if company exists
        company = self.db.query(Company).filter(
            Company.name_normalized == normalized_company_name
        ).first()

        if not company:
            # Create new company
            company = Company(
                name=normalized_company_name,
                name_normalized=normalized_company_name,
            )
            self.db.add(company)
            self.db.flush()  # Get ID without committing

        return company
