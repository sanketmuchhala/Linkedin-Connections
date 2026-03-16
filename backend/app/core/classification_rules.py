"""
Classification rules for detecting job functions, seniority, and flags.
All rules are deterministic heuristics based on keywords.
"""
from typing import Dict, List


class ClassificationRules:
    """Heuristic rules for connection classification."""

    # Job Function Keywords
    ENGINEERING_KEYWORDS = [
        "engineer", "developer", "programmer", "architect", "sde", "sdet",
        "software", "devops", "backend", "frontend", "full stack", "fullstack",
        "embedded", "systems", "infrastructure", "platform"
    ]

    DATA_SCIENCE_KEYWORDS = [
        "data scientist", "machine learning", "ai engineer", "ml engineer",
        "data analyst", "analytics", "data engineer", "mlops", "ai",
        "artificial intelligence", "deep learning", "computer vision", "nlp",
        "natural language", "statistician"
    ]

    PRODUCT_KEYWORDS = [
        "product manager", "product owner", "pm", "product lead",
        "product director", "chief product", "head of product"
    ]

    DESIGN_KEYWORDS = [
        "designer", "ux", "ui", "design", "user experience", "user interface",
        "graphic designer", "visual designer", "product designer"
    ]

    MARKETING_KEYWORDS = [
        "marketing", "brand", "growth", "content", "digital marketing",
        "social media", "seo", "sem", "campaign", "communications"
    ]

    SALES_KEYWORDS = [
        "sales", "business development", "bdr", "account executive", "sdr",
        "sales engineer", "account manager", "sales manager", "revenue"
    ]

    HR_KEYWORDS = [
        "recruiter", "talent", "human resources", "hr", "people operations",
        "people partner", "talent acquisition", "sourcer", "staffing"
    ]

    OPERATIONS_KEYWORDS = [
        "operations", "ops", "supply chain", "logistics", "procurement",
        "facilities", "administration", "office manager"
    ]

    FINANCE_KEYWORDS = [
        "finance", "accounting", "accountant", "controller", "treasurer",
        "financial analyst", "investment", "portfolio", "risk"
    ]

    LEGAL_KEYWORDS = [
        "attorney", "lawyer", "counsel", "legal", "compliance", "regulatory"
    ]

    EXECUTIVE_KEYWORDS = [
        "chief", "ceo", "cto", "cfo", "coo", "cmo", "cpo", "ciso", "cdo",
        "president", "founder", "co-founder", "cofounder", "partner",
        "managing director", "chairman", "board member"
    ]

    # Seniority Keywords (check in order of precedence)
    FOUNDER_KEYWORDS = ["founder", "co-founder", "cofounder"]

    C_LEVEL_KEYWORDS = [
        "chief", "ceo", "cto", "cfo", "coo", "cmo", "cpo", "ciso", "cdo",
        "chief executive", "chief technology", "chief financial", "chief operating"
    ]

    VP_KEYWORDS = ["vice president", "vp", "svp", "evp", "senior vice president"]

    DIRECTOR_KEYWORDS = ["director", "head of", "senior director"]

    MANAGER_KEYWORDS = [
        "manager", "lead", "team lead", "group manager", "senior manager",
        "program manager", "project manager"
    ]

    SENIOR_KEYWORDS = [
        "senior", "sr", "principal", "staff", "senior engineer", "senior developer"
    ]

    JUNIOR_KEYWORDS = [
        "junior", "jr", "associate", "entry level", "entry-level"
    ]

    INTERN_KEYWORDS = ["intern", "internship", "co-op"]

    # Boolean Flag Keywords
    RECRUITER_KEYWORDS = [
        "recruiter", "talent acquisition", "talent partner", "sourcer",
        "staffing", "headhunter", "talent specialist"
    ]

    AI_ML_KEYWORDS = [
        "machine learning", "ml engineer", "ai engineer", "deep learning",
        "nlp", "computer vision", "artificial intelligence", "generative ai",
        "genai", "llm", "large language model", "neural network",
        "data scientist", "ai researcher", "ml researcher"
    ]

    STUDENT_KEYWORDS = [
        "student", "graduate assistant", "research assistant",
        "teaching assistant", "undergraduate", "graduate student", "phd student"
    ]

    RESEARCHER_KEYWORDS = [
        "researcher", "research scientist", "research engineer", "phd",
        "postdoc", "research associate"
    ]

    # University/College keywords for company-based student detection
    UNIVERSITY_KEYWORDS = [
        "university", "college", "school", "institute", "academy", "ucl", "mit"
    ]

    @classmethod
    def contains_any(cls, text: str, keywords: List[str]) -> bool:
        """Check if text contains any of the keywords (case-insensitive)."""
        if not text:
            return False
        text_lower = text.lower()
        return any(keyword.lower() in text_lower for keyword in keywords)

    @classmethod
    def get_job_function(cls, position: str) -> str:
        """
        Classify job function based on position title.

        Args:
            position: Normalized position title

        Returns:
            Job function category (JobFunction enum value)
        """
        if not position:
            return "other"

        # Check in order of specificity
        # Executive check first (highest priority)
        if cls.contains_any(position, cls.EXECUTIVE_KEYWORDS):
            return "executive"

        # Data Science (before Engineering as some keywords overlap)
        if cls.contains_any(position, cls.DATA_SCIENCE_KEYWORDS):
            return "data_science"

        # Engineering
        if cls.contains_any(position, cls.ENGINEERING_KEYWORDS):
            return "engineering"

        # Product
        if cls.contains_any(position, cls.PRODUCT_KEYWORDS):
            return "product"

        # Design
        if cls.contains_any(position, cls.DESIGN_KEYWORDS):
            return "design"

        # HR
        if cls.contains_any(position, cls.HR_KEYWORDS):
            return "hr"

        # Sales
        if cls.contains_any(position, cls.SALES_KEYWORDS):
            return "sales"

        # Marketing
        if cls.contains_any(position, cls.MARKETING_KEYWORDS):
            return "marketing"

        # Finance
        if cls.contains_any(position, cls.FINANCE_KEYWORDS):
            return "finance"

        # Legal
        if cls.contains_any(position, cls.LEGAL_KEYWORDS):
            return "legal"

        # Operations
        if cls.contains_any(position, cls.OPERATIONS_KEYWORDS):
            return "operations"

        return "other"

    @classmethod
    def get_seniority_level(cls, position: str) -> str:
        """
        Classify seniority level based on position title.

        Check in order of precedence (highest to lowest).

        Args:
            position: Normalized position title

        Returns:
            Seniority level (SeniorityLevel enum value)
        """
        if not position:
            return "mid"

        # Check in order of precedence
        if cls.contains_any(position, cls.FOUNDER_KEYWORDS):
            return "founder"

        if cls.contains_any(position, cls.C_LEVEL_KEYWORDS):
            return "c_level"

        if cls.contains_any(position, cls.VP_KEYWORDS):
            return "vp"

        if cls.contains_any(position, cls.DIRECTOR_KEYWORDS):
            return "director"

        if cls.contains_any(position, cls.MANAGER_KEYWORDS):
            return "manager"

        if cls.contains_any(position, cls.SENIOR_KEYWORDS):
            return "senior"

        if cls.contains_any(position, cls.JUNIOR_KEYWORDS):
            return "junior"

        if cls.contains_any(position, cls.INTERN_KEYWORDS):
            return "intern"

        # Default to mid-level
        return "mid"

    @classmethod
    def is_recruiter(cls, position: str) -> bool:
        """Check if position is a recruiter role."""
        return cls.contains_any(position, cls.RECRUITER_KEYWORDS)

    @classmethod
    def is_founder(cls, position: str) -> bool:
        """Check if position indicates founder status."""
        return cls.contains_any(position, cls.FOUNDER_KEYWORDS)

    @classmethod
    def is_cxo(cls, position: str) -> bool:
        """Check if position is C-level executive."""
        return cls.contains_any(position, cls.C_LEVEL_KEYWORDS)

    @classmethod
    def is_ai_ml(cls, position: str, company: str = "") -> bool:
        """
        Check if position/company is AI/ML related.

        Args:
            position: Normalized position title
            company: Normalized company name

        Returns:
            True if AI/ML related
        """
        return cls.contains_any(position, cls.AI_ML_KEYWORDS) or \
               cls.contains_any(company, cls.AI_ML_KEYWORDS)

    @classmethod
    def is_engineer(cls, position: str) -> bool:
        """Check if position is an engineering role."""
        return cls.contains_any(position, cls.ENGINEERING_KEYWORDS)

    @classmethod
    def is_student(cls, position: str, company: str = "") -> bool:
        """
        Check if connection is a student.

        Student if:
        - Position contains student keywords, OR
        - Company is a university AND position contains "assistant"

        Args:
            position: Normalized position title
            company: Normalized company name

        Returns:
            True if student
        """
        if cls.contains_any(position, cls.STUDENT_KEYWORDS):
            return True

        # Check for research/teaching assistants at universities
        if cls.contains_any(company, cls.UNIVERSITY_KEYWORDS):
            if "assistant" in position.lower():
                return True

        return False

    @classmethod
    def is_researcher(cls, position: str) -> bool:
        """Check if position is a research role."""
        return cls.contains_any(position, cls.RESEARCHER_KEYWORDS)
