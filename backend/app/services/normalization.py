"""
Normalization service for cleaning and standardizing data.
"""
import re
from typing import Dict, Optional
import pandas as pd


class NormalizationService:
    """Normalize names, companies, and titles using deterministic heuristics."""

    # Common titles and credentials to remove from names
    NAME_TITLES = [
        "Dr.", "PhD", "Ph.D", "MBA", "FRM", "CFA", "PE", "PMP", "CPA", "MD",
        "Mr.", "Mrs.", "Ms.", "Miss", "Jr.", "Sr.", "III", "IV", "Esq.",
    ]

    # Company name mappings for common variations
    COMPANY_MAPPINGS = {
        # Universities
        r"Indiana University.*": "Indiana University",
        r"IU\s.*": "Indiana University",
        r"Carnegie Mellon.*": "Carnegie Mellon University",
        r"MIT\s.*": "Massachusetts Institute of Technology",
        r"Stanford University.*": "Stanford University",

        # Big Tech
        r"Microsoft Corp.*": "Microsoft",
        r"Amazon\.com.*": "Amazon",
        r"Meta Platforms.*": "Meta",
        r"Facebook.*": "Meta",
        r"Google LLC.*": "Google",
        r"Alphabet Inc.*": "Google",
        r"Apple Inc.*": "Apple",

        # Banks & Financial
        r"JPMorgan.*": "JPMorgan Chase",
        r"Goldman Sachs.*": "Goldman Sachs",
        r"Morgan Stanley.*": "Morgan Stanley",
        r"Bank of America.*": "Bank of America",

        # Stealth/Startup
        r"Stealth.*": "Stealth Startup",
    }

    # Legal suffixes to remove
    LEGAL_SUFFIXES = [
        r",?\s*Inc\.?$",
        r",?\s*LLC\.?$",
        r",?\s*Ltd\.?$",
        r",?\s*Limited$",
        r",?\s*Corporation$",
        r",?\s*Corp\.?$",
        r",?\s*L\.P\.?$",
        r",?\s*LLP\.?$",
    ]

    # Title abbreviation mappings
    TITLE_ABBREVS = {
        r"\bVP\b": "Vice President",
        r"\bAVP\b": "Assistant Vice President",
        r"\bSVP\b": "Senior Vice President",
        r"\bEVP\b": "Executive Vice President",
        r"\bCEO\b": "Chief Executive Officer",
        r"\bCTO\b": "Chief Technology Officer",
        r"\bCFO\b": "Chief Financial Officer",
        r"\bCOO\b": "Chief Operating Officer",
        r"\bCMO\b": "Chief Marketing Officer",
        r"\bCPO\b": "Chief Product Officer",
        r"\bCISO\b": "Chief Information Security Officer",
        r"\bSr\.?": "Senior",
        r"\bJr\.?": "Junior",
        r"\bMgr\.?": "Manager",
        r"\bDir\.?": "Director",
        r"\bEng\.?": "Engineer",
        r"\bDev\.?": "Developer",
        r"\bSWE\b": "Software Engineer",
    }

    def normalize_row(self, row: Dict) -> Dict:
        """
        Apply all normalization rules to a row.

        Args:
            row: Raw connection record

        Returns:
            Dictionary with normalized fields
        """
        first_name = row.get("First Name", "")
        last_name = row.get("Last Name", "")

        return {
            "first_name_normalized": self.normalize_name(first_name),
            "last_name_normalized": self.normalize_name(last_name),
            "full_name_normalized": self.normalize_full_name(first_name, last_name),
            "company_normalized": self.normalize_company(row.get("Company")),
            "position_normalized": self.normalize_position(row.get("Position")),
        }

    def normalize_name(self, name: Optional[str]) -> str:
        """
        Normalize person name.

        - Remove titles/credentials (Dr., PhD, MBA, etc.)
        - Remove special characters
        - Title case
        - Handle "undefined" (some LinkedIn exports have this)

        Args:
            name: Raw name string

        Returns:
            Normalized name
        """
        if not name or pd.isna(name):
            return ""

        # Handle "undefined" case
        if name.lower() == "undefined":
            return ""

        # Remove titles and credentials
        normalized = name
        for title in self.NAME_TITLES:
            # Case-insensitive replacement
            normalized = re.sub(r'\b' + re.escape(title) + r'\b', '', normalized, flags=re.IGNORECASE)

        # Remove special characters except spaces, hyphens, and apostrophes
        normalized = re.sub(r'[^a-zA-Z\s\-\']', '', normalized)

        # Normalize whitespace
        normalized = " ".join(normalized.split())

        # Title case
        normalized = normalized.strip().title()

        return normalized

    def normalize_full_name(self, first_name: Optional[str], last_name: Optional[str]) -> str:
        """
        Create normalized full name from first and last names.

        Args:
            first_name: Raw first name
            last_name: Raw last name

        Returns:
            Normalized full name
        """
        first = self.normalize_name(first_name)
        last = self.normalize_name(last_name)

        if first and last:
            return f"{first} {last}"
        elif first:
            return first
        elif last:
            return last
        else:
            return "Unknown"

    def normalize_company(self, company: Optional[str]) -> str:
        """
        Normalize company name.

        - Handle common variations using mappings
        - Remove legal suffixes (Inc., LLC, etc.)
        - Standardize known companies

        Args:
            company: Raw company name

        Returns:
            Normalized company name
        """
        if not company or pd.isna(company):
            return ""

        normalized = company.strip()

        # Apply company mappings
        for pattern, replacement in self.COMPANY_MAPPINGS.items():
            if re.match(pattern, normalized, re.IGNORECASE):
                return replacement

        # Remove legal suffixes
        for suffix in self.LEGAL_SUFFIXES:
            normalized = re.sub(suffix, "", normalized, flags=re.IGNORECASE)

        # Clean up extra whitespace
        normalized = " ".join(normalized.split())

        return normalized.strip()

    def normalize_position(self, position: Optional[str]) -> str:
        """
        Normalize job title/position.

        - Expand abbreviations (VP → Vice President)
        - Remove special formatting
        - Standardize common patterns

        Args:
            position: Raw position title

        Returns:
            Normalized position title
        """
        if not position or pd.isna(position):
            return ""

        normalized = position

        # Expand abbreviations
        for abbrev, full in self.TITLE_ABBREVS.items():
            normalized = re.sub(abbrev, full, normalized, flags=re.IGNORECASE)

        # Clean up extra whitespace
        normalized = " ".join(normalized.split())

        return normalized.strip()

    def extract_company_type_hint(self, company: str) -> Optional[str]:
        """
        Extract hints about company type from company name.

        Args:
            company: Normalized company name

        Returns:
            Company type hint (startup, university, etc.) or None
        """
        if not company:
            return None

        company_lower = company.lower()

        # University indicators
        if any(word in company_lower for word in ["university", "college", "institute", "school"]):
            return "university"

        # Startup indicators
        if "stealth" in company_lower:
            return "startup"

        # Big tech (add more as needed)
        big_tech = [
            "google", "microsoft", "amazon", "meta", "apple", "netflix",
            "facebook", "alphabet", "tesla", "nvidia"
        ]
        if any(company_lower == tech or company_lower.startswith(tech + " ") for tech in big_tech):
            return "big_tech"

        return None
