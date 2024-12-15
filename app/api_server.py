from fastapi import FastAPI
from app.routers import energy
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "API is running"}

# Include routers
app.include_router(energy.router, prefix="/energy")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")
