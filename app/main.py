from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, events, organizations, pathways, programs, search

app = FastAPI(
    title="Innovation POC API",
    description="API for Innovation POC application",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api")  # Mount auth at /api/auth
app.include_router(events.router, prefix="/api/events", tags=["events"])
app.include_router(organizations.router, prefix="/api/organizations", tags=["organizations"])
app.include_router(pathways.router, prefix="/api/pathways", tags=["pathways"])
app.include_router(programs.router, prefix="/api/programs", tags=["programs"])
app.include_router(search.router, prefix="/api/search", tags=["search"])

@app.get("/")
async def root():
    return {"message": "Innovation POC API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

