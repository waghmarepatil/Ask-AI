from db.database import engine, Base

# Creates all tables from models
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)