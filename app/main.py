from fastapi import FastAPI
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Finance Dashboard API",
    description="Backend API for finance data processing and access control",
    version="1.0.0",
)


@app.get("/", tags=["Health"])
def health_check():
    """Health check endpoint to verify the API is running."""
    return {"status": "ok", "message": "Finance Dashboard API is running"}
