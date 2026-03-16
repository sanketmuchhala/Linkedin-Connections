"""
Test script to import LinkedIn Connections CSV.
"""
import sys
sys.path.insert(0, '/Users/sanketmuchhala/Documents/GitHub/Linkedin Connections/backend')

from app.database import SessionLocal, init_db
from app.services.data_pipeline import DataPipeline

# Initialize database
init_db()

# Create database session
db = SessionLocal()

# Path to CSV file
csv_path = "/Users/sanketmuchhala/Documents/GitHub/Linkedin Connections/Connections.csv"

print(f"🚀 Starting import of {csv_path}...")
print("-" * 80)

# Create pipeline and process CSV
pipeline = DataPipeline(db)

# Create default scoring config
pipeline.create_default_scoring_config()

# Process CSV
result = pipeline.process_csv(csv_path, overwrite=True)

if result.success:
    print("\n" + "=" * 80)
    print("✨ IMPORT SUCCESSFUL!")
    print("=" * 80)
    print(f"\n📊 Summary:")
    print(f"   Total connections processed: {result.processed_count}")
    print(f"   Unique companies: {result.summary.get('unique_companies', 0)}")
    print(f"   With email: {result.summary.get('with_email', 0)} ({result.summary.get('email_percentage', 0)}%)")
    print(f"   With company: {result.summary.get('with_company', 0)} ({result.summary.get('company_percentage', 0)}%)")
    print(f"   With position: {result.summary.get('with_position', 0)} ({result.summary.get('position_percentage', 0)}%)")
else:
    print("\n" + "=" * 80)
    print("❌ IMPORT FAILED!")
    print("=" * 80)
    print(f"\n📛 Errors:")
    for error in result.errors:
        print(f"   - {error}")

# Close database session
db.close()

print("\n✅ Test complete!")
