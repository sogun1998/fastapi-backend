from fastapi import FastAPI
from app.database import engine, Base
from app.controllers.authors import router as authors_router
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(authors_router)
