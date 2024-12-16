from fastapi import FastAPI
from app.utils.data_client import fetch_climate_data
from app.routers import energy

app = FastAPI()

app.include_router(energy.router, prefix="/energy", tags=["Energy"])

@app.get("/")
def health_check():
    return{"status": "API is running"}

@app.get("/climate-data")
def get_climate_data():
    try:
        data = fetch_climate_data()
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)