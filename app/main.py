from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import events, organizations, pathways, search

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Innovation Zone Ecosystem API",
    description="API for Windsor-Essex Innovation Ecosystem Platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(events.router, prefix="/api/events", tags=["events"])
app.include_router(organizations.router, prefix="/api/organizations", tags=["organizations"])
app.include_router(pathways.router, prefix="/api/pathways", tags=["pathways"])
app.include_router(search.router, prefix="/api/search", tags=["search"])

@app.get("/")
async def root():
    return {"message": "Innovation Zone Ecosystem API", "version": "1.0.0"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

