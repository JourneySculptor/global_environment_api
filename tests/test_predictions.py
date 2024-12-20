from fastapi.testclient import TestClient
from app.api_server import app

client = TestClient(app)

def test_forecast_renewable_energy():
    """
    Test the /energy/forecast/renewable-energy endpoint.

    Ensures that the forecast returns valid data and a graph URL.
    """
    response = client.get("/energy/forecast/renewable-energy?country=USA&years=5")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data
    assert "graph_url" in data
