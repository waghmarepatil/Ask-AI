from db.database import AsyncSessionLocal

#Creates DB session per request
async def get_db():
    #Open session and auto close session
    async with AsyncSessionLocal() as session:
        #FastAPI handles lifecycle
        yield session