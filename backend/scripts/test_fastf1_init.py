from app.services.fastf1_service import FastF1Service
from app.core.database import SessionLocal
import asyncio

def main():
    db = SessionLocal()
    service = FastF1Service(db)
    # 只拉取 2023 年数据，避免数据量过大
    asyncio.run(service.initialize_database(2023, 2023))
    db.close()

if __name__ == "__main__":
    main() 