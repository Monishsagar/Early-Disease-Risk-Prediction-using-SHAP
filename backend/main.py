"""
FastAPI main application.
Entry point for the Early Disease Risk Prediction backend.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import sys

# Import routes
from routes.predict import router as predict_router
from routes.datasets import router as datasets_router
from routes.health import router as health_router
from models.train import load_or_train_all_models

# Global state for models
app_state = {
    "models": {},
    "metadata": {}
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    # Startup: Train/load all models
    print("\n" + "="*80)
    print("🚀 INITIALIZING EARLY DISEASE RISK PREDICTION API")
    print("="*80)
    
    try:
        models, metadata = load_or_train_all_models(force_retrain=False)
        app_state["models"] = models
        app_state["metadata"] = metadata
        print("\n✓ API READY - All models loaded successfully!")
        print("="*80 + "\n")
    except Exception as e:
        print(f"\n✗ STARTUP FAILED: {e}")
        print("="*80 + "\n")
        sys.exit(1)
    
    yield
    
    # Shutdown
    print("\n🛑 Shutting down API...")


# Create FastAPI app
app = FastAPI(
    title="Early Disease Risk Prediction API",
    description="AI-powered clinical decision support for early disease risk assessment",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health_router)
app.include_router(predict_router)
app.include_router(datasets_router)


@app.get("/")
async def root():
    """
    Root endpoint - API information.
    """
    return {
        "name": "Early Disease Risk Prediction API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "GET /api/health",
            "predict": "POST /api/predict/{disease}",
            "dataset_stats": "GET /api/dataset/stats/{disease}",
            "docs": "/docs",
            "openapi": "/openapi.json"
        },
        "diseases": ["heart", "diabetes", "liver", "kidney"]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )
