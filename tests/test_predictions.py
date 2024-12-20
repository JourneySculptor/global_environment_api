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


def test_export_forecast_csv():
    """
    Test exporting forecast data as a CSV file.
    """
    response = client.get("/energy/export/forecast?country=JPN&years=5&format=csv")
    assert response.status_code == 200  # Check response status
    assert "text/csv" in response.headers["content-type"]  # Partial match for charset
    assert "attachment; filename=\"JPN_forecast.csv\"" in response.headers["content-disposition"]


def test_export_forecast_excel():
    """
    Test exporting forecast data as an Excel file.
    """
    response = client.get("/energy/export/forecast?country=JPN&years=5&format=excel")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    assert "attachment; filename=\"JPN_forecast.xlsx\"" in response.headers["content-disposition"]


def test_export_forecast_pdf():
    """
    Test exporting forecast data as a PDF file.
    """
    response = client.get("/energy/export/forecast?country=JPN&years=5&format=pdf")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert "attachment; filename=\"JPN_forecast.pdf\"" in response.headers["content-disposition"]
