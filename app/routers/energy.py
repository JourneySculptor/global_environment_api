import os
import logging
import matplotlib.pyplot as plt
from io import BytesIO
from fastapi.responses import Response, FileResponse
from fastapi import APIRouter, HTTPException, Query
from google.cloud import bigquery
import matplotlib
from pydantic import BaseModel
from typing import List

# Define a Pydantic model for climate data response
class ClimateDataItem(BaseModel):
    year: int
    temp: float
    country: str

class ClimateDataResponse(BaseModel):
    status: str
    data: List[dict]

# Initialize FastAPI router
router = APIRouter()

# Non-GUI backend for Matplotlib
matplotlib.use("Agg") 

# Logging Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Directory for saving graphs
GRAPH_FOLDER = "static/graphs"
if not os.path.exists(GRAPH_FOLDER):
    os.makedirs(GRAPH_FOLDER)

# Initialize BigQuery client
client = bigquery.Client()

# Add this function to improve error handling
def handle_exception(e: Exception, detail: str = "An error occurred"):
    """Log the error and return an HTTPException."""
    logger.error(f"{detail}: {e}")
    raise HTTPException(status_code=500, detail=detail)

# Modify this existing function in energy.py
def fetch_data_from_bigquery(query: str):
    """Fetch data from BigQuery with robust error handling."""
    try:
        query_job = client.query(query)
        return query_job.result()
    except Exception as e:
        handle_exception(e, "Error fetching data from BigQuery")

def save_chart_and_return_path(buf, filename: str):
    """Save chart buffer to file and return the file path."""
    file_path = os.path.join(GRAPH_FOLDER, filename)
    with open(file_path, "wb") as f:
        f.write(buf.getvalue())
    logger.info(f"Chart saved at: {file_path}")
    return file_path

def generate_pie_chart(labels, values, title: str):
    """Generate a pie chart."""
    plt.figure(figsize=(10, 6))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title(title)
    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return buf

def generate_bar_chart(x_values, y_values, title: str, x_label: str, y_label: str):
    """Generate a bar chart."""
    plt.figure(figsize=(12, 7))
    plt.bar(x_values, y_values, color='skyblue')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xticks(rotation=45)
    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return buf

def generate_line_chart(x_values, y_values, title: str, x_label: str, y_label: str):
    """Generate a line chart."""
    plt.figure(figsize=(12, 7))
    plt.plot(x_values, y_values, marker='o', linestyle='-', color='b')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xticks(rotation=45)
    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return buf

# ------------------------------
# Endpoints with Save Functionality
# ------------------------------

@router.get(
    "/energy/climate-data",
    response_model=ClimateDataResponse,
    responses={404: {"description": "Data not found"}}
)
async def get_climate_data(
    year: int = Query(None, description="Year to filter data"), 
    country: str = Query(None, description="Country code to filter data")
):
    """Fetch global climate data with optional filters for year and country."""
    # Start with a base query
    query = """
        SELECT year, average_temperature, country
        FROM `global-environment-project.climate_data.global_temperature`
        WHERE TRUE
    """

    # Add filters dynamically, ensuring proper formatting
    if year:
        query += f" AND year = {year}"
    if country:
        query += f" AND country = '{country}'"

    query += " ORDER BY year DESC"

    logger.info(f"Executing query: {query}") 

    # Fetch data
    results = fetch_data_from_bigquery(query)
    if not results.total_rows:
        logger.warning("No data found for the climate data query.")
        return {"status": "success", "data": [], "message": "No data found for the given filters."}

    # Format and return data
    data = [{"year": row.year, "temp": row.average_temperature, "country": row.country} for row in results]
    return {"status": "success", "data": data}

@router.get("/energy/renewable-energy/{country_code}")
async def get_renewable_energy(country_code: str):
    """Fetch renewable energy data by country."""
    query = f"""
        SELECT Year, `Country Name`, Renewable_Energy_Consumption
        FROM `global-environment-project.renewable_energy_data.renewable_energy_consumption`
        WHERE `Country Code` = '{country_code}'
        ORDER BY Year DESC
    """
    results = fetch_data_from_bigquery(query)
    
    # Return an empty response if no data is found
    if not results.total_rows:
        logger.warning("No data found for the climate data query.")
        return {"status": "success", "data": [], "message": "No data found for the given filters."}

    data = [{"Year": row.Year, "Country": row["Country Name"], "Consumption": row.Renewable_Energy_Consumption} for row in results]
    return {"status": "success", "data": data}


@router.get("/energy/graph/pie/renewable-energy/{year}")
async def get_pie_chart_renewable_energy(year: int):
    """Generate and return a pie chart for renewable energy consumption."""
    query = f"""
        SELECT `Country Name`, Renewable_Energy_Consumption
        FROM `global-environment-project.renewable_energy_data.renewable_energy_consumption`
        WHERE Year = {year}
        ORDER BY Renewable_Energy_Consumption DESC
        LIMIT 10
    """
    results = fetch_data_from_bigquery(query)
    
    # Return an empty response if no data is found
    if not results.total_rows:
        logger.warning("No data found for the query.")
        return {"status": "success", "data": [], "message": "No data found for the given filters."}

    countries, consumption = zip(*[(row["Country Name"], row.Renewable_Energy_Consumption) for row in results])
    buf = generate_pie_chart(countries, consumption, f"Top 10 Renewable Energy Consumers in {year}")
    file_path = save_chart_and_return_path(buf, f"top_10_renewable_{year}.png")
    return FileResponse(file_path, media_type="image/png")


@router.get("/energy/graph/bar/renewable-energy/{country_code}")
async def get_bar_chart_renewable_energy(country_code: str):
    """Generate and return a bar chart for renewable energy consumption."""
    query = f"""
        SELECT Year, Renewable_Energy_Consumption
        FROM `global-environment-project.renewable_energy_data.renewable_energy_consumption`
        WHERE `Country Code` = '{country_code}'
        ORDER BY Year ASC
    """
    results = fetch_data_from_bigquery(query)
    
    # Return an empty response if no data is found
    if not results.total_rows:
        logger.warning("No data found for the climate data query.")
        return {"status": "success", "data": [], "message": "No data found for the given filters."}

    years, consumption = zip(*[(row.Year, row.Renewable_Energy_Consumption) for row in results])
    buf = generate_bar_chart(years, consumption, f"Renewable Energy Consumption in {country_code}", "Year", "Consumption (%)")
    file_path = save_chart_and_return_path(buf, f"{country_code}_bar_chart.png")
    return FileResponse(file_path, media_type="image/png")


@router.get("/energy/graph/line/renewable-energy/{country_code}")
async def get_line_chart_renewable_energy(country_code: str):
    """Generate and return a line chart for renewable energy consumption."""
    query = f"""
        SELECT Year, Renewable_Energy_Consumption
        FROM `global-environment-project.renewable_energy_data.renewable_energy_consumption`
        WHERE `Country Code` = '{country_code}'
        ORDER BY Year ASC
    """
    results = fetch_data_from_bigquery(query)
    
    # Return an empty response if no data is found
    if not results.total_rows:
        logger.warning("No data found for the climate data query.")
        return {"status": "success", "data": [], "message": "No data found for the given filters."}

    years, consumption = zip(*[(row.Year, row.Renewable_Energy_Consumption) for row in results])
    buf = generate_line_chart(years, consumption, f"Renewable Energy Consumption Over Time in {country_code}", "Year", "Consumption (%)")
    file_path = save_chart_and_return_path(buf, f"{country_code}_line_chart.png")
    return FileResponse(file_path, media_type="image/png")
