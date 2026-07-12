import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .db import init_db
from .routes import docs, search, qa, examples, troubleshoot, best_practices

app = FastAPI(
    title="DocRAG API",
    description="Developer Documentation Technical Assistant Backend",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(docs.router, prefix="/api")
app.include_router(search.router, prefix="/api")
app.include_router(qa.router, prefix="/api")
app.include_router(examples.router, prefix="/api")
app.include_router(troubleshoot.router, prefix="/api")
app.include_router(best_practices.router, prefix="/api")

@app.on_event("startup")
def startup_event():
    init_db()
    print("DocRAG database initialized successfully.")

@app.get("/")
def read_root():
    return {"message": "Welcome to DocRAG API server."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=settings.BACKEND_PORT, reload=True)
