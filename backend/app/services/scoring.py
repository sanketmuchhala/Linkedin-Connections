"""
Scoring service for calculating connection priority scores.
"""
from typing import Dict, Optional
from datetime import datetime, date


class ScoringService:
    """Calculate weighted scores for connections with transparent explanations."""

    # Default scoring configuration
    DEFAULT_CONFIG = {
        "base_weights": {
            "seniority": 0.30,
            "function": 0.25,
            "recency": 0.20,
            "company": 0.15,
            "email": 0.10,
        },
        "seniority_scores": {
            "intern": 10,
            "junior": 20,
            "mid": 40,
            "senior": 60,
            "lead": 70,
            "manager": 75,
            "director": 85,
            "vp": 90,
            "c_level": 95,
            "founder": 100,
        },
        "function_scores": {
            "data_science": 85,
            "engineering": 80,
            "executive": 90,
            "product": 70,
            "design": 60,
            "operations": 50,
            "finance": 50,
            "sales": 40,
            "marketing": 40,
            "hr": 30,
            "legal": 50,
            "other": 50,
        },
        "flag_bonuses": {
            "is_ai_ml": 15,
            "is_founder": 20,
            "is_cxo": 15,
            "is_recruiter": -10,
            "is_engineer_and_ai_ml": 5,
            "dense_company": 5,
        },
    }

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize scoring service with configuration.

        Args:
            config: Scoring configuration dict (uses default if None)
        """
        self.config = config or self.DEFAULT_CONFIG

    def calculate_scores(self, row: Dict, company_connection_count: int = 0) -> Dict:
        """
        Calculate all scores for a connection with breakdown.

        Args:
            row: Connection record with classification results
            company_connection_count: Number of connections at this company

        Returns:
            Dictionary with scores and breakdown
        """
        weights = self.config["base_weights"]

        # Calculate component scores
        seniority_score = self._get_seniority_score(row.get("seniority_level"))
        function_score = self._get_function_score(row.get("job_function"))
        recency_score = self._calculate_recency_score(row.get("connected_on"))
        company_score = 60  # Default company score (can be enhanced later)
        email_score = 5 if row.get("email_address") else 0

        # Calculate base score (weighted sum)
        base_score = (
            seniority_score * weights["seniority"] +
            function_score * weights["function"] +
            recency_score * weights["recency"] +
            company_score * weights["company"] +
            email_score * weights["email"]
        )

        # Calculate flag bonuses
        bonuses = {}
        total_bonus = 0

        if row.get("is_ai_ml"):
            bonus = self.config["flag_bonuses"]["is_ai_ml"]
            bonuses["is_ai_ml"] = bonus
            total_bonus += bonus

        if row.get("is_founder"):
            bonus = self.config["flag_bonuses"]["is_founder"]
            bonuses["is_founder"] = bonus
            total_bonus += bonus

        if row.get("is_cxo"):
            bonus = self.config["flag_bonuses"]["is_cxo"]
            bonuses["is_cxo"] = bonus
            total_bonus += bonus

        if row.get("is_recruiter"):
            bonus = self.config["flag_bonuses"]["is_recruiter"]
            bonuses["is_recruiter"] = bonus
            total_bonus += bonus

        # Combo bonus: Engineer + AI/ML
        if row.get("is_engineer") and row.get("is_ai_ml"):
            bonus = self.config["flag_bonuses"]["is_engineer_and_ai_ml"]
            bonuses["engineer_and_ai_ml"] = bonus
            total_bonus += bonus

        # Dense company bonus (5+ connections at same company)
        if company_connection_count >= 5:
            bonus = self.config["flag_bonuses"]["dense_company"]
            bonuses["dense_company"] = bonus
            total_bonus += bonus

        # Calculate total score (capped at 100)
        total_score = min(base_score + total_bonus, 100)

        # Generate explanation
        explanation = self._generate_explanation(row, total_score)

        # Create breakdown
        breakdown = {
            "base": round(base_score, 1),
            "components": {
                "seniority": round(seniority_score, 1),
                "function": round(function_score, 1),
                "recency": round(recency_score, 1),
                "company": round(company_score, 1),
                "email": round(email_score, 1),
            },
            "bonuses": bonuses,
            "total_bonus": round(total_bonus, 1),
            "total": round(total_score, 1),
            "explanation": explanation,
        }

        return {
            "outreach_score": round(total_score, 1),
            "relevance_score": round(self._calculate_relevance_score(row), 1),
            "influence_score": round(self._calculate_influence_score(row), 1),
            "total_score": round(total_score, 1),
            "score_breakdown": breakdown,
        }

    def _get_seniority_score(self, seniority_level: Optional[str]) -> float:
        """Get score for seniority level."""
        if not seniority_level:
            return 40  # Default mid-level

        return self.config["seniority_scores"].get(seniority_level, 40)

    def _get_function_score(self, job_function: Optional[str]) -> float:
        """Get score for job function."""
        if not job_function:
            return 50  # Default

        return self.config["function_scores"].get(job_function, 50)

    def _calculate_recency_score(self, connected_on: Optional[date]) -> float:
        """
        Calculate score based on how recently connected.

        Scoring:
        - ≤30 days: 100
        - ≤90 days: 80
        - ≤180 days: 60
        - ≤365 days: 40
        - >365 days: 20

        Args:
            connected_on: Date of connection

        Returns:
            Recency score (0-100)
        """
        if not connected_on:
            return 20  # Very old or unknown

        # Handle both date and datetime objects
        if isinstance(connected_on, datetime):
            connected_on = connected_on.date()

        today = date.today()
        days_ago = (today - connected_on).days

        if days_ago <= 30:
            return 100
        elif days_ago <= 90:
            return 80
        elif days_ago <= 180:
            return 60
        elif days_ago <= 365:
            return 40
        else:
            return 20

    def _calculate_relevance_score(self, row: Dict) -> float:
        """
        Calculate relevance score based on target role fit.

        For now, this is similar to outreach score but focused on role match.

        Args:
            row: Connection record

        Returns:
            Relevance score (0-100)
        """
        score = 50  # Base

        # High relevance for AI/ML + Engineering
        if row.get("is_ai_ml") and row.get("is_engineer"):
            score += 30
        elif row.get("is_ai_ml"):
            score += 20
        elif row.get("is_engineer"):
            score += 15

        # Bonus for data science
        if row.get("job_function") == "data_science":
            score += 15

        # Founder/Executive bonus
        if row.get("is_founder"):
            score += 10
        elif row.get("is_cxo"):
            score += 5

        return min(score, 100)

    def _calculate_influence_score(self, row: Dict) -> float:
        """
        Calculate influence score based on seniority and role.

        Args:
            row: Connection record

        Returns:
            Influence score (0-100)
        """
        seniority_level = row.get("seniority_level", "mid")
        score = self._get_seniority_score(seniority_level)

        # Boost for founders and executives
        if row.get("is_founder"):
            score = min(score + 20, 100)
        elif row.get("is_cxo"):
            score = min(score + 15, 100)

        return score

    def _generate_explanation(self, row: Dict, score: float) -> str:
        """
        Generate human-readable explanation for the score.

        Args:
            row: Connection record
            score: Calculated total score

        Returns:
            Explanation string
        """
        parts = []

        # Seniority
        seniority = row.get("seniority_level", "mid").replace("_", " ").title()
        parts.append(seniority)

        # Function
        function = row.get("job_function", "").replace("_", " ").title()
        if function and function != "Other":
            parts.append(function)

        # Key flags
        if row.get("is_founder"):
            parts.append("Founder")
        elif row.get("is_cxo"):
            parts.append("C-level Executive")

        if row.get("is_ai_ml"):
            parts.append("AI/ML")

        # Company
        company = row.get("company_normalized", "")
        if company:
            parts.append(f"at {company}")

        if score >= 80:
            priority = "High-priority outreach target"
        elif score >= 60:
            priority = "Good outreach potential"
        elif score >= 40:
            priority = "Moderate priority"
        else:
            priority = "Lower priority"

        return f"{priority}: {' - '.join(parts)}"
