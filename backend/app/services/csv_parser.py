"""
CSV Parser service for LinkedIn Connections CSV files.
"""
import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime
import re


class ValidationError:
    """Represents a validation error in the CSV."""

    def __init__(self, row: int, field: str, message: str):
        self.row = row
        self.field = field
        self.message = message

    def __repr__(self):
        return f"Row {self.row}, Field '{self.field}': {self.message}"


class CSVParser:
    """Parse and validate LinkedIn Connections CSV files."""

    REQUIRED_COLUMNS = [
        "First Name",
        "Last Name",
        "URL",
        "Connected On",
    ]

    OPTIONAL_COLUMNS = [
        "Email Address",
        "Company",
        "Position",
    ]

    def parse(self, file_path: str) -> List[Dict]:
        """
        Parse CSV file into list of dictionaries.

        Args:
            file_path: Path to the CSV file

        Returns:
            List of connection records as dictionaries

        Raises:
            ValueError: If required columns are missing or file cannot be parsed
        """
        try:
            # Read CSV, skipping the first 3 rows (LinkedIn's header notes)
            df = pd.read_csv(file_path, skiprows=3)

            # Validate required columns exist
            missing_cols = set(self.REQUIRED_COLUMNS) - set(df.columns)
            if missing_cols:
                raise ValueError(f"Missing required columns: {', '.join(missing_cols)}")

            # Replace NaN with None for cleaner handling
            df = df.where(pd.notna(df), None)

            # Convert to list of dictionaries
            records = df.to_dict('records')

            return records

        except Exception as e:
            raise ValueError(f"Failed to parse CSV file: {str(e)}")

    def validate(self, records: List[Dict]) -> List[ValidationError]:
        """
        Validate each record in the parsed data.

        Note: This now only returns warnings, not blocking errors.
        Invalid rows will be skipped during import.

        Args:
            records: List of connection records

        Returns:
            List of validation warnings
        """
        warnings = []

        for idx, record in enumerate(records):
            row_num = idx + 5  # Actual row in CSV (accounting for header + skiprows)

            # Check required fields (warnings only)
            if not record.get("First Name") or not record.get("Last Name"):
                warnings.append(ValidationError(row_num, "Name", "Missing name - row will be skipped"))

            # Validate URL format (warnings only)
            url = record.get("URL", "")
            if url and not self._is_valid_linkedin_url(url):
                warnings.append(ValidationError(row_num, "URL", "Invalid LinkedIn URL - row will be skipped"))

            # Validate date format (warnings only)
            connected_on = record.get("Connected On")
            if connected_on and not self._is_valid_date(connected_on):
                warnings.append(ValidationError(row_num, "Connected On", "Invalid date - will use default"))

        return warnings

    def is_valid_record(self, record: Dict) -> bool:
        """
        Check if a record is valid enough to import.

        Args:
            record: Connection record

        Returns:
            True if record has minimum required fields
        """
        # Must have first name, last name, and valid URL
        if not record.get("First Name") or not record.get("Last Name"):
            return False

        url = record.get("URL", "")
        if not url or not self._is_valid_linkedin_url(url):
            return False

        return True

    def _is_valid_linkedin_url(self, url: str) -> bool:
        """Check if URL is a valid LinkedIn profile URL."""
        if not url:
            return False

        # LinkedIn profile URLs follow pattern: https://www.linkedin.com/in/[username]
        pattern = r'^https://www\.linkedin\.com/in/[\w\-]+/?$'
        return bool(re.match(pattern, url))

    def _is_valid_date(self, date_str: str) -> bool:
        """Check if date string is in valid format (DD MMM YYYY)."""
        if not date_str:
            return False

        try:
            # Try parsing with LinkedIn's date format
            datetime.strptime(date_str, "%d %b %Y")
            return True
        except ValueError:
            return False

    def parse_date(self, date_str: str) -> Optional[datetime]:
        """
        Parse LinkedIn date string to datetime object.

        Args:
            date_str: Date string in format "DD MMM YYYY"

        Returns:
            datetime object or None if invalid
        """
        if not date_str:
            return None

        try:
            return datetime.strptime(date_str, "%d %b %Y")
        except ValueError:
            return None

    def get_summary(self, records: List[Dict]) -> Dict:
        """
        Get summary statistics for parsed records.

        Args:
            records: List of connection records

        Returns:
            Dictionary with summary stats
        """
        total = len(records)
        with_email = sum(1 for r in records if r.get("Email Address"))
        with_company = sum(1 for r in records if r.get("Company"))
        with_position = sum(1 for r in records if r.get("Position"))

        return {
            "total_records": total,
            "with_email": with_email,
            "with_company": with_company,
            "with_position": with_position,
            "email_percentage": round(with_email / total * 100, 1) if total > 0 else 0,
            "company_percentage": round(with_company / total * 100, 1) if total > 0 else 0,
            "position_percentage": round(with_position / total * 100, 1) if total > 0 else 0,
        }
