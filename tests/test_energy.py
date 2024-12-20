import pytest
from fastapi.testclient import TestClient
from app.api_server import app
import sys
import os

# Set sys.path to include the project root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

client = TestClient(app)

# Test for normal /energy/climate-data
def test_climate_data():
    """Test /energy/climate-data endpoint."""
    response = client.get("/energy/climate-data")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["data"]) > 0

# Test for /energy/renewable-energy/{country_code}
def test_renewable_energy_by_country():
    """Test /energy/renewable-energy/{country_code} endpoint."""
    response = client.get("/energy/renewable-energy/JPN")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["data"]) > 0
    

# Test for /energy/graph/bar/renewable-energy/{country_code}
def test_renewable_energy_bar_chart():
    """Test /energy/graph/bar/renewable-energy/{country_code} endpoint."""
    response = client.get("/energy/graph/bar/renewable-energy/JPN")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"

# Test for /energy/graph/line/renewable-energy/{country_code}
def test_renewable_energy_line_chart():
    """Test /energy/graph/line/renewable-energy/{country_code} endpoint."""
    response = client.get("/energy/graph/line/renewable-energy/JPN")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    assert os.path.exists(os.path.join("static/graphs", "JPN_line_chart.png"))

# New tests for empty results
def test_climate_data_no_results(monkeypatch):
    """Test /energy/climate-data with no results."""
    def mock_fetch_data_from_bigquery(query):
        class MockResult:
            total_rows = 0
        return MockResult()
    
    monkeypatch.setattr("app.routers.energy.fetch_data_from_bigquery", mock_fetch_data_from_bigquery)
    
    response = client.get("/energy/climate-data")
    assert response.status_code == 200
    assert response.json() == {"status": "success", "data": []}

def test_renewable_energy_no_results(monkeypatch):
    """Test /energy/renewable-energy/{country_code} with no results."""
    def mock_fetch_data_from_bigquery(query):
        class MockResult:
            total_rows = 0
        return MockResult()
    
    monkeypatch.setattr("app.routers.energy.fetch_data_from_bigquery", mock_fetch_data_from_bigquery)
    
    response = client.get("/energy/renewable-energy/JPN")
    assert response.status_code == 200
    assert response.json() == {"status": "success", "data": []}

def test_pie_chart_no_results(monkeypatch):
    """Test /energy/graph/pie/renewable-energy/{year} with no results."""
    def mock_fetch_data_from_bigquery(query):
        class MockResult:
            total_rows = 0
        return MockResult()
    
    monkeypatch.setattr("app.routers.energy.fetch_data_from_bigquery", mock_fetch_data_from_bigquery)
    
    response = client.get("/energy/graph/pie/renewable-energy/2022")
    assert response.status_code == 200
    assert response.json() == {"status": "success", "data": []}

def test_bar_chart_no_results(monkeypatch):
    """Test /energy/graph/bar/renewable-energy/{country_code} with no results."""
    def mock_fetch_data_from_bigquery(query):
        class MockResult:
            total_rows = 0
        return MockResult()
    
    monkeypatch.setattr("app.routers.energy.fetch_data_from_bigquery", mock_fetch_data_from_bigquery)
    
    response = client.get("/energy/graph/bar/renewable-energy/JPN")
    assert response.status_code == 200
    assert response.json() == {"status": "success", "data": []}

def test_line_chart_no_results(monkeypatch):
    """Test /energy/graph/line/renewable-energy/{country_code} with no results."""
    def mock_fetch_data_from_bigquery(query):
        class MockResult:
            total_rows = 0
        return MockResult()
    
    monkeypatch.setattr("app.routers.energy.fetch_data_from_bigquery", mock_fetch_data_from_bigquery)
    
    response = client.get("/energy/graph/line/renewable-energy/JPN")
    assert response.status_code == 200
    assert response.json() == {"status": "success", "data": []}
