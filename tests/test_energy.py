import pytest
from fastapi.testclient import TestClient
import sys
import os

# Set sys.path to include the parent directory of the app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.api_server import app  # Import app after fixing sys.path

client = TestClient(app)

def test_read_root():
    """
    Test root endpoint.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "API is running"}

def test_climate_data():
    """
    Test /energy/climate-data endpoint.
    """
    response = client.get("/energy/climate-data")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data
    assert len(data["data"]) > 0

def test_renewable_energy_by_country():
    """
    Test /energy/renewable-energy/{country_code} endpoint.
    """
    response = client.get("/energy/renewable-energy/JPN")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data
    assert len(data["data"]) > 0
    assert data["data"][0]["Country"] == "Japan"

def test_renewable_energy_by_year():
    """
    Test /energy/renewable-energy/year/{year} endpoint.
    """
    response = client.get("/energy/renewable-energy/year/2021")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data
    assert len(data["data"]) > 0
    assert data["data"][0]["Year"] == 2021

def test_renewable_energy_by_country_and_year():
    """
    Test /energy/renewable-energy/{country_code}/{year} endpoint.
    """
    response = client.get("/energy/renewable-energy/JPN/2021")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data
    assert len(data["data"]) == 1
    assert data["data"][0]["Year"] == 2021
    assert data["data"][0]["Country"] == "Japan"
