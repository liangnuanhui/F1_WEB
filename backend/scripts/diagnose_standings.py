import os
import sys
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy import create_engine

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.config import Settings
from app.models.standings import DriverStanding

def diagnose_query():
    """
    Connects to the database and performs a targeted query to diagnose the issue.
    """
    print("--- Starting Standings Diagnosis ---")
    
    try:
        # Get database settings
        settings = Settings()
        db_url = str(settings.database_url)
        print(f"Connecting to database: {db_url}")

        # Create engine and session
        engine = create_engine(db_url, pool_pre_ping=True)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        print("Database session created successfully.")

    except Exception as e:
        print("\n--- ERROR DURING DATABASE SETUP ---")
        print(f"An error occurred while setting up the database connection: {e}")
        print("Please check your .env file and database configuration.")
        return

    try:
        print("\n--- Performing Query ---")
        print("Attempting to fetch the first DriverStanding record with driver and constructor info...")

        # The exact query that is failing in the API
        first_standing = db.query(DriverStanding).options(
            joinedload(DriverStanding.driver),
            joinedload(DriverStanding.constructor)
        ).first()

        if not first_standing:
            print("\n--- QUERY RESULT: EMPTY ---")
            print("The DriverStanding table appears to be empty.")
            print("This could be the issue. Please ensure data has been initialized.")
            return

        print("\n--- QUERY RESULT: SUCCESS ---")
        print("Successfully fetched a record from DriverStanding.")
        
        print("\n--- Accessing Record Attributes ---")
        
        # Try to access all relevant attributes one by one
        print(f"Accessing position: {first_standing.position}")
        print(f"Accessing points: {first_standing.points}")
        
        print("Accessing driver relationship...")
        if first_standing.driver:
            print("  -> Driver object exists.")
            print(f"  -> Accessing driver name: {first_standing.driver.forename} {first_standing.driver.surname}")
        else:
            print("  -> WARNING: Driver relationship is None!")

        print("Accessing constructor relationship...")
        if first_standing.constructor:
            print("  -> Constructor object exists.")
            print(f"  -> Accessing constructor name: {first_standing.constructor.name}")
        else:
             print("  -> WARNING: Constructor relationship is None!")

        print("\n--- DIAGNOSIS COMPLETE ---")
        print("The script was able to query the database and access related data without errors.")
        print("If you are still seeing 500 errors, the problem might be within the FastAPI application lifecycle itself (e.g., dependency injection, response model validation).")

    except Exception as e:
        print("\n--- ERROR DURING QUERY OR DATA ACCESS ---")
        import traceback
        traceback.print_exc()
        print(f"\nAn error occurred: {e}")
        print("This is the likely source of the 500 error.")
        
    finally:
        if 'db' in locals() and db:
            db.close()
            print("\nDatabase session closed.")

if __name__ == "__main__":
    diagnose_query() 