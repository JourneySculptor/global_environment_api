import pytest
from fastapi.testclient import TestClient
from app.api_server import app
import os

# Setup TestClient
client = TestClient(app)

# Base URL for static files
STATIC_DIR = "static/graphs"


# Test climate data endpoint
def test_climate_data():
    """Test /energy/climate-data endpoint."""
    response = client.get("/energy/climate-data")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["data"]) > 0


# Test renewable energy data by country
def test_renewable_energy_by_country():
    """Test /energy/renewable-energy/{country_code} endpoint."""
    response = client.get("/energy/renewable-energy/JPN")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["data"]) > 0


# Test bar chart generation
def test_renewable_energy_bar_chart():
    """Test /energy/graph/bar/renewable-energy/{country_code} endpoint."""
    response = client.get("/energy/graph/bar/renewable-energy/JPN")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    assert os.path.exists(os.path.join(STATIC_DIR, "JPN_bar_chart.png"))


# Test line chart generation
def test_renewable_energy_line_chart():
    """Test /energy/graph/line/renewable-energy/{country_code} endpoint."""
    response = client.get("/energy/graph/line/renewable-energy/JPN")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    assert os.path.exists(os.path.join(STATIC_DIR, "JPN_line_chart.png"))


# Test forecast endpoint
def test_forecast_renewable_energy():
    """Test /energy/forecast/renewable-energy?country=JPN&years=5 endpoint."""
    response = client.get("/energy/forecast/renewable-energy?country=JPN&years=5")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["data"]) == 5
    assert "graph_url" in data


# Test no results scenario with monkeypatch
def test_climate_data_no_results(monkeypatch):
    """Test /energy/climate-data when no data is found."""
    class MockResult:
        total_rows = 0  # Mock the total_rows attribute to simulate no results

    def mock_fetch_data(query):
        return MockResult()  # Return the mocked result

    monkeypatch.setattr("app.routers.energy.fetch_data_from_bigquery", mock_fetch_data)

    response = client.get("/energy/climate-data")
    assert response.status_code == 200
    assert response.json() == {"status": "success", "data": []}

