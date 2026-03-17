"""
Data pipeline orchestrator for processing LinkedIn connections CSV.
"""
from sqlalchemy.orm import Session
from typing import Dict, List
from .csv_parser import CSVParser
from .normalization import NormalizationService
from .classification import ClassificationService
from .scoring import ScoringService
from .company_aggregation import CompanyAggregationService
from ..models import Connection, ScoringConfig
from datetime import datetime


class ProcessingResult:
    """Result of data processing pipeline."""

    def __init__(
        self,
        success: bool,
        processed_count: int = 0,
        errors: List = None,
        summary: Dict = None,
        connections: List = None,
    ):
        self.success = success
        self.processed_count = processed_count
        self.errors = errors or []
        self.summary = summary or {}
        self.connections = connections or []


class DataPipeline:
    """Orchestrate the entire data processing pipeline."""

    def __init__(self, db: Session):
        """
        Initialize pipeline with database session.

        Args:
            db: SQLAlchemy database session
        """
        self.db = db
        self.csv_parser = CSVParser()
        self.normalizer = NormalizationService()
        self.classifier = ClassificationService()
        self.scorer = ScoringService()
        self.aggregator = CompanyAggregationService(db)

    def process_csv(
        self,
        file_path: str,
        overwrite: bool = False
    ) -> ProcessingResult:
        """
        Execute the full data processing pipeline.

        Pipeline steps:
        1. Parse and validate CSV
        2. Normalize data (names, companies, titles)
        3. Classify connections (function, seniority, flags)
        4. Calculate scores (weighted algorithm)
        5. Store in database
        6. Aggregate company metrics

        Args:
            file_path: Path to the LinkedIn Connections CSV file
            overwrite: If True, delete existing data before import

        Returns:
            ProcessingResult with status and details
        """
        try:
            # Step 1: Parse and validate CSV
            print("Parsing CSV file...")
            parsed_data = self.csv_parser.parse(file_path)
            validation_warnings = self.csv_parser.validate(parsed_data)

            if validation_warnings:
                print(f"Found {len(validation_warnings)} warnings (invalid rows will be skipped)")

            # Filter out invalid records
            valid_records = [r for r in parsed_data if self.csv_parser.is_valid_record(r)]
            skipped_count = len(parsed_data) - len(valid_records)

            if skipped_count > 0:
                print(f"Skipping {skipped_count} invalid rows")

            # Get summary stats
            summary = self.csv_parser.get_summary(valid_records)
            summary['skipped_rows'] = skipped_count
            print(f"Parsed {len(valid_records)} valid records")
            parsed_data = valid_records  # Use only valid records

            # If overwrite, delete existing data
            if overwrite:
                print("Deleting existing connections...")
                self.db.query(Connection).delete()
                self.db.commit()

            # Step 2: Normalize data
            print("Normalizing data...")
            for row in parsed_data:
                normalized = self.normalizer.normalize_row(row)
                row.update(normalized)

            # Step 3: Classify connections
            print("Classifying connections...")
            for row in parsed_data:
                classification = self.classifier.classify(row)
                row.update(classification)

            # Step 4: Calculate scores
            print("Calculating scores...")
            # Get active scoring config
            active_config = self.get_active_scoring_config()

            for row in parsed_data:
                # Note: company connection count will be updated later
                scores = self.scorer.calculate_scores(row, company_connection_count=0)
                row.update(scores)

            # Step 5: Store in database
            print("Storing connections in database...")
            connections = []
            for row in parsed_data:
                conn = self.upsert_connection(row)
                if conn:
                    connections.append(conn)

            # Commit all connections
            self.db.commit()
            print(f"Stored {len(connections)} connections")

            # Step 6: Recalculate scores with company connection counts
            print("Recalculating scores with company data...")
            self.recalculate_scores_with_company_data(connections, active_config)

            # Step 7: Aggregate company metrics
            print("Aggregating company metrics...")
            self.aggregator.recalculate_all_companies()
            self.db.commit()

            summary.update({
                "total_processed": len(connections),
                "unique_companies": self.db.query(Connection.company_id).distinct().count(),
            })

            print(f"Processing complete! {len(connections)} connections processed.")

            return ProcessingResult(
                success=True,
                processed_count=len(connections),
                summary=summary,
                connections=connections,
            )

        except Exception as e:
            print(f"Error during processing: {str(e)}")
            self.db.rollback()
            return ProcessingResult(
                success=False,
                errors=[str(e)],
                summary={"error": str(e)}
            )

    def upsert_connection(self, row: Dict) -> Connection:
        """
        Insert or update a connection in the database.

        Args:
            row: Processed connection data

        Returns:
            Connection model instance
        """
        linkedin_url = row.get("URL")

        if not linkedin_url:
            return None

        # Check if connection already exists
        connection = self.db.query(Connection).filter(
            Connection.linkedin_url == linkedin_url
        ).first()

        # Parse date
        connected_on_str = row.get("Connected On")
        connected_on = self.csv_parser.parse_date(connected_on_str)

        if connection:
            # Update existing connection
            self._update_connection_from_row(connection, row, connected_on)
        else:
            # Create new connection
            connection = self._create_connection_from_row(row, connected_on)
            self.db.add(connection)

        # Get or create company
        company_normalized = row.get("company_normalized")
        if company_normalized:
            company = self.aggregator.create_or_update_company(company_normalized)
            connection.company = company

        connection.last_processed_at = datetime.utcnow()

        return connection

    def _create_connection_from_row(self, row: Dict, connected_on: datetime) -> Connection:
        """Create a new Connection instance from row data."""
        return Connection(
            # Raw data
            first_name_raw=row.get("First Name", ""),
            last_name_raw=row.get("Last Name", ""),
            linkedin_url=row.get("URL", ""),
            email_address=row.get("Email Address"),
            company_raw=row.get("Company"),
            position_raw=row.get("Position"),
            connected_on=connected_on,

            # Normalized data
            first_name_normalized=row.get("first_name_normalized", ""),
            last_name_normalized=row.get("last_name_normalized", ""),
            full_name_normalized=row.get("full_name_normalized", ""),
            company_normalized=row.get("company_normalized"),
            position_normalized=row.get("position_normalized"),

            # Classification
            job_function=row.get("job_function"),
            seniority_level=row.get("seniority_level"),
            is_recruiter=row.get("is_recruiter", False),
            is_founder=row.get("is_founder", False),
            is_cxo=row.get("is_cxo", False),
            is_ai_ml=row.get("is_ai_ml", False),
            is_engineer=row.get("is_engineer", False),
            is_student=row.get("is_student", False),
            is_researcher=row.get("is_researcher", False),

            # Scores
            outreach_score=row.get("outreach_score", 0.0),
            relevance_score=row.get("relevance_score", 0.0),
            influence_score=row.get("influence_score", 0.0),
            total_score=row.get("total_score", 0.0),
            score_breakdown=row.get("score_breakdown"),

            # Outreach status
            outreach_status="not_contacted",
        )

    def _update_connection_from_row(self, connection: Connection, row: Dict, connected_on: datetime):
        """Update an existing Connection instance from row data."""
        # Update raw data
        connection.first_name_raw = row.get("First Name", "")
        connection.last_name_raw = row.get("Last Name", "")
        connection.email_address = row.get("Email Address")
        connection.company_raw = row.get("Company")
        connection.position_raw = row.get("Position")
        connection.connected_on = connected_on

        # Update normalized data
        connection.first_name_normalized = row.get("first_name_normalized", "")
        connection.last_name_normalized = row.get("last_name_normalized", "")
        connection.full_name_normalized = row.get("full_name_normalized", "")
        connection.company_normalized = row.get("company_normalized")
        connection.position_normalized = row.get("position_normalized")

        # Update classification
        connection.job_function = row.get("job_function")
        connection.seniority_level = row.get("seniority_level")
        connection.is_recruiter = row.get("is_recruiter", False)
        connection.is_founder = row.get("is_founder", False)
        connection.is_cxo = row.get("is_cxo", False)
        connection.is_ai_ml = row.get("is_ai_ml", False)
        connection.is_engineer = row.get("is_engineer", False)
        connection.is_student = row.get("is_student", False)
        connection.is_researcher = row.get("is_researcher", False)

        # Update scores
        connection.outreach_score = row.get("outreach_score", 0.0)
        connection.relevance_score = row.get("relevance_score", 0.0)
        connection.influence_score = row.get("influence_score", 0.0)
        connection.total_score = row.get("total_score", 0.0)
        connection.score_breakdown = row.get("score_breakdown")

    def recalculate_scores_with_company_data(self, connections: List[Connection], active_config):
        """
        Recalculate scores after company data is available.

        This adds the "dense company" bonus for companies with 5+ connections.

        Args:
            connections: List of Connection instances
            active_config: Active scoring configuration
        """
        # Group connections by company
        from collections import defaultdict
        company_connections = defaultdict(list)

        for conn in connections:
            if conn.company_id:
                company_connections[conn.company_id].append(conn)

        # Recalculate scores for connections at dense companies
        for company_id, conns in company_connections.items():
            if len(conns) >= 5:
                # This is a "dense company" - recalculate scores with bonus
                scorer = ScoringService(active_config)

                for conn in conns:
                    # Create row dict from connection
                    row = {
                        "seniority_level": conn.seniority_level,
                        "job_function": conn.job_function,
                        "connected_on": conn.connected_on,
                        "email_address": conn.email_address,
                        "is_ai_ml": conn.is_ai_ml,
                        "is_founder": conn.is_founder,
                        "is_cxo": conn.is_cxo,
                        "is_recruiter": conn.is_recruiter,
                        "is_engineer": conn.is_engineer,
                        "company_normalized": conn.company_normalized,
                    }

                    # Recalculate with company connection count
                    scores = scorer.calculate_scores(row, company_connection_count=len(conns))

                    # Update connection scores
                    conn.outreach_score = scores["outreach_score"]
                    conn.relevance_score = scores["relevance_score"]
                    conn.influence_score = scores["influence_score"]
                    conn.total_score = scores["total_score"]
                    conn.score_breakdown = scores["score_breakdown"]

    def get_active_scoring_config(self) -> Dict:
        """
        Get the active scoring configuration.

        Returns:
            Scoring config dict (or default if none active)
        """
        active_config = self.db.query(ScoringConfig).filter(
            ScoringConfig.is_active == True
        ).first()

        if active_config:
            return active_config.weights

        # Return default config from scorer
        return self.scorer.DEFAULT_CONFIG

    def create_default_scoring_config(self):
        """Create the default scoring configuration in the database."""
        # Check if default config exists
        default_config = self.db.query(ScoringConfig).filter(
            ScoringConfig.name == "Default"
        ).first()

        if not default_config:
            default_config = ScoringConfig(
                name="Default",
                description="Default scoring configuration for LinkedIn connections",
                is_active=True,
                weights=self.scorer.DEFAULT_CONFIG,
            )
            self.db.add(default_config)
            self.db.commit()
