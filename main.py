from fastapi import FastAPI
from contextlib import asynccontextmanager
from dotenv import load_dotenv


from app.api.routes import router
from app.services.rag_service import rag_engine

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # start RAG engine and load data on startup
    rag_engine.initialize_engine()
    yield
    print("Shutting down AI Engine...")

# init FastAPI app with metadata and lifespan handler for startup/shutdown events
app = FastAPI(
    title="Loblaw Merchandise Analytics RAG API",
    description="A modular, production-grade microservice for extracting retail insights.",
    version="2.0.0",
    lifespan=lifespan
)

# connect API routes
app.include_router(router, prefix="/api/v1")