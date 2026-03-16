"""
Classification service for categorizing connections.
"""
from typing import Dict
from ..core.classification_rules import ClassificationRules


class ClassificationService:
    """Classify connections using rule-based heuristics."""

    def __init__(self):
        self.rules = ClassificationRules()

    def classify(self, row: Dict) -> Dict:
        """
        Apply all classification rules to a normalized row.

        Args:
            row: Dictionary with normalized fields (position_normalized, company_normalized)

        Returns:
            Dictionary with classification results
        """
        position = row.get("position_normalized", "")
        company = row.get("company_normalized", "")

        # Get job function and seniority
        job_function = self.rules.get_job_function(position)
        seniority_level = self.rules.get_seniority_level(position)

        # Get boolean flags
        is_recruiter = self.rules.is_recruiter(position)
        is_founder = self.rules.is_founder(position)
        is_cxo = self.rules.is_cxo(position)
        is_ai_ml = self.rules.is_ai_ml(position, company)
        is_engineer = self.rules.is_engineer(position)
        is_student = self.rules.is_student(position, company)
        is_researcher = self.rules.is_researcher(position)

        return {
            "job_function": job_function,
            "seniority_level": seniority_level,
            "is_recruiter": is_recruiter,
            "is_founder": is_founder,
            "is_cxo": is_cxo,
            "is_ai_ml": is_ai_ml,
            "is_engineer": is_engineer,
            "is_student": is_student,
            "is_researcher": is_researcher,
        }

    def classify_batch(self, rows: list[Dict]) -> list[Dict]:
        """
        Classify multiple rows.

        Args:
            rows: List of normalized records

        Returns:
            List of classification results
        """
        return [self.classify(row) for row in rows]
