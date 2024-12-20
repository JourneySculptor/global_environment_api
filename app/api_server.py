from fastapi import FastAPI
from app.routers import energy, predictions
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import sys
import os

# Load environment variables from .env
load_dotenv()

# Test if the variable is loaded correctly
print(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

app = FastAPI()

# Register energy router
app.include_router(energy.router, tags=["energy"]) 

# Register predictions router
app.include_router(predictions.router, tags=["predictions"])

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return {"status": "API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")
