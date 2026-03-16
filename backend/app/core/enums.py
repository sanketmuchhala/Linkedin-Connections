"""
Enums for the LinkedIn Intelligence application.
"""
from enum import Enum


class JobFunction(str, Enum):
    """Job function categories."""
    ENGINEERING = "engineering"
    DATA_SCIENCE = "data_science"
    PRODUCT = "product"
    DESIGN = "design"
    MARKETING = "marketing"
    SALES = "sales"
    HR = "hr"
    OPERATIONS = "operations"
    EXECUTIVE = "executive"
    FINANCE = "finance"
    LEGAL = "legal"
    OTHER = "other"


class SeniorityLevel(str, Enum):
    """Seniority levels."""
    INTERN = "intern"
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    MANAGER = "manager"
    DIRECTOR = "director"
    VP = "vp"
    C_LEVEL = "c_level"
    FOUNDER = "founder"


class CompanyType(str, Enum):
    """Company type categories."""
    STARTUP = "startup"
    BIG_TECH = "big_tech"
    ENTERPRISE = "enterprise"
    UNIVERSITY = "university"
    UNKNOWN = "unknown"


class OutreachType(str, Enum):
    """Types of outreach activities."""
    MESSAGE = "message"
    EMAIL = "email"
    MEETING = "meeting"
    CALL = "call"
    REFERRAL = "referral"
    OTHER = "other"


class OutreachStatus(str, Enum):
    """Status of outreach activities."""
    PLANNED = "planned"
    SENT = "sent"
    REPLIED = "replied"
    MEETING_SCHEDULED = "meeting_scheduled"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"
    NO_RESPONSE = "no_response"
