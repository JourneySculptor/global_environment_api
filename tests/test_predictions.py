import pytest
from fastapi.testclient import TestClient
from app.api_server import app

# Initialize test client
client = TestClient(app)

# Test: Forecast endpoint with missing parameters
def test_forecast_missing_parameters():
    """
    Test forecast endpoint with missing parameters.
    """
    response = client.get("/energy/forecast/renewable-energy")
    assert response.status_code == 422  # Unprocessable Entity
    assert "detail" in response.json()

# Test: Invalid country code
def test_forecast_invalid_country():
    """
    Test forecast endpoint with an invalid country code.
    """
    response = client.get("/energy/forecast/renewable-energy?country=XYZ&years=5")
    assert response.status_code == 404  # Not Found
    assert response.json()["detail"] == "No data found for the given country."

# Test: Years parameter exceeds limit
def test_forecast_years_exceed_limit():
    """
    Test forecast endpoint when 'years' parameter exceeds limit.
    """
    response = client.get("/energy/forecast/renewable-energy?country=JPN&years=100")
    assert response.status_code == 400  # Bad Request
    assert response.json()["detail"] == "Years parameter exceeds allowed range."

# Test: Valid response with exact forecast
def test_forecast_valid():
    """
    Test valid forecast request with correct parameters.
    """
    response = client.get("/energy/forecast/renewable-energy?country=JPN&years=5")
    assert response.status_code == 200  # Success
    data = response.json()
    assert data["status"] == "success"
    assert len(data["data"]) == 5  # 5 years forecast
    assert "graph_url" in data  # Graph URL should exist
