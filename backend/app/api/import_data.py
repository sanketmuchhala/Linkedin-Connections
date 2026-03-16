"""
Import data API endpoints.
"""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from pathlib import Path
import uuid
import os
from ..database import get_db
from ..services.data_pipeline import DataPipeline

router = APIRouter()


@router.post("/csv")
async def import_csv(
    file: UploadFile = File(...),
    overwrite: bool = False,
    db: Session = Depends(get_db),
):
    """
    Import LinkedIn Connections CSV file.

    Args:
        file: Uploaded CSV file
        overwrite: If True, delete existing data before import
        db: Database session

    Returns:
        Import result with summary
    """
    # Validate file type
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    # Create uploads directory if it doesn't exist
    upload_dir = Path("data/uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)

    # Save uploaded file with unique name
    file_id = str(uuid.uuid4())
    file_path = upload_dir / f"{file_id}_{file.filename}"

    try:
        # Write file to disk
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        # Process with data pipeline
        pipeline = DataPipeline(db)
        result = pipeline.process_csv(str(file_path), overwrite=overwrite)

        # Clean up uploaded file
        os.unlink(file_path)

        if not result.success:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Import failed",
                    "errors": [str(e) for e in result.errors],
                }
            )

        return {
            "success": True,
            "message": f"Successfully imported {result.processed_count} connections",
            "summary": result.summary,
        }

    except Exception as e:
        # Clean up file if it exists
        if file_path.exists():
            os.unlink(file_path)

        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
def get_import_status(db: Session = Depends(get_db)):
    """
    Get current import status and database statistics.

    Returns:
        Database statistics
    """
    from ..models import Connection, Company

    total_connections = db.query(Connection).count()
    total_companies = db.query(Company).count()

    return {
        "total_connections": total_connections,
        "total_companies": total_companies,
        "status": "ready",
    }
