# This file can be used to initialize the database when starting the app.
import asyncio
from app.db.models import init_db

if __name__ == "__main__":
    asyncio.run(init_db())
