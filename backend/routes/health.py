"""
Health check API route.
GET /api/health - Check API status
"""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api", tags=["health"])


class HealthResponse(BaseModel):
    status: str


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Check API health status.
    """
    return HealthResponse(status="ok")
