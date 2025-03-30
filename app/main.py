from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api.routes import router
from app.config import settings

# Create FastAPI application
app = FastAPI(
    title="Whois Domain Lookup API",
    description="API for looking up domain and contact information using Whois",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(router)

# Create a root endpoint
@app.get("/", include_in_schema=False)
async def root():
    """Root endpoint."""
    return {"message": "Welcome to Whois Domain Lookup API. Go to /api/docs for documentation."}


if __name__ == "__main__":
    """Run the application with uvicorn."""
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=5000,
        reload=settings.RELOAD,
    )

