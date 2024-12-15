import os
import logging
import matplotlib.pyplot as plt
from io import BytesIO
from fastapi.responses import Response, FileResponse
from fastapi import APIRouter, HTTPException
from google.cloud import bigquery

# Initialize FastAPI router
router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Graph storage directory configuration
GRAPH_FOLDER = "static/graphs"
if not os.path.exists(GRAPH_FOLDER):
    os.makedirs(GRAPH_FOLDER)

# Initialize BigQuery client
client = bigquery.Client()

# ------------------------------
# Existing Endpoints for Data Fetching
# ------------------------------

@router.get("/climate-data")
async def get_climate_data():
    """
    Fetch and return climate data from BigQuery.
    """
    try:
        query = """
            SELECT year, average_temperature, country
            FROM `global-environment-project.climate_data.global_temperature`
            ORDER BY year DESC
        """
        query_job = client.query(query)
        results = [
            {
                "year": row.year,
                "average_temperature": row.average_temperature,
                "country": row.country
            }
            for row in query_job.result()
        ]
        return {"status": "success", "data": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching climate data: {str(e)}")


@router.get("/renewable-energy/{country_code}")
async def get_renewable_energy(country_code: str):
    """
    Fetch renewable energy data for a specific country.
    """
    try:
        query = f"""
            SELECT *
            FROM `global-environment-project.renewable_energy_data.renewable_energy_consumption`
            WHERE `Country Code` = '{country_code}'
            ORDER BY Year DESC
        """
        query_job = client.query(query)
        results = [
            {
                "Year": row.Year,
                "Country": row["Country Name"],
                "Renewable Energy Consumption": row.Renewable_Energy_Consumption,
            }
            for row in query_job.result()
        ]
        return {"status": "success", "data": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data for {country_code}: {str(e)}")


@router.get("/renewable-energy/year/{year}")
async def get_energy_by_year(year: int):
    """
    Fetch renewable energy data for a specific year.
    """
    try:
        query = f"""
            SELECT *
            FROM `global-environment-project.renewable_energy_data.renewable_energy_consumption`
            WHERE Year = {year}
            ORDER BY `Country Code` ASC
        """
        query_job = client.query(query)
        results = [
            {
                "Year": row.Year,
                "Country": row["Country Name"],
                "Renewable Energy Consumption": row.Renewable_Energy_Consumption,
            }
            for row in query_job.result()
        ]
        return {"status": "success", "data": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data for year {year}: {str(e)}")


@router.get("/renewable-energy/{country_code}/{year}")
async def get_energy_by_country_and_year(country_code: str, year: int):
    """
    Fetch renewable energy data for a specific country and year.
    """
    try:
        query = f"""
            SELECT *
            FROM `global-environment-project.renewable_energy_data.renewable_energy_consumption`
            WHERE `Country Code` = '{country_code}' AND Year = {year}
        """
        query_job = client.query(query)
        results = [
            {
                "Year": row.Year,
                "Country": row["Country Name"],
                "Renewable Energy Consumption": row.Renewable_Energy_Consumption,
            }
            for row in query_job.result()
        ]
        return {"status": "success", "data": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data for {country_code} in {year}: {str(e)}")

# ------------------------------
# New Endpoints for Graph Generation
# ------------------------------

@router.get("/graph/renewable-energy/{country_code}")
async def get_renewable_energy_graph(country_code: str):
    """
    Generate a graph for renewable energy consumption, return it as an image, and save it locally.
    """
    try:
        logger.debug(f"Fetching renewable energy data for country code: {country_code}")

        # BigQuery SQL query
        query = f"""
            SELECT Year, Renewable_Energy_Consumption
            FROM `global-environment-project.renewable_energy_data.renewable_energy_consumption`
            WHERE `Country Code` = '{country_code}'
            ORDER BY Year ASC
        """
        query_job = client.query(query)
        results = query_job.result()

        # Extract data for plotting
        years = []
        consumption = []
        for row in results:
            years.append(row["Year"])
            consumption.append(row["Renewable_Energy_Consumption"])

        if not years or not consumption:
            logger.warning(f"No data found for country code: {country_code}")
            raise HTTPException(status_code=404, detail="No data found for the specified country")

        # Generate the graph
        plt.figure(figsize=(10, 6))
        plt.plot(years, consumption, marker='o', linestyle='-', color='b')
        plt.title(f"Renewable Energy Consumption in {country_code}")
        plt.xlabel("Year")
        plt.ylabel("Renewable Energy Consumption (%)")
        plt.grid(True)

        # Save the graph to the specified folder
        graph_filename = f"{country_code}_renewable_energy.png"
        graph_path = os.path.join(GRAPH_FOLDER, graph_filename)
        plt.savefig(graph_path)
        plt.close()

        logger.info(f"Graph saved at: {graph_path}")

        # Return the graph as an HTTP response
        return FileResponse(graph_path, media_type="image/png")

    except Exception as e:
        logger.error(f"Error generating graph for {country_code}: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating graph for {country_code}: {str(e)}")


@router.get("/graph/save/renewable-energy/{country_code}")
async def save_renewable_energy_graph(country_code: str):
    """
    Generate and save a graph for renewable energy consumption to a file.
    """
    try:
        # Query renewable energy data
        query = f"""
            SELECT Year, Renewable_Energy_Consumption
            FROM `global-environment-project.renewable_energy_data.renewable_energy_consumption`
            WHERE `Country Code` = '{country_code}'
            ORDER BY Year ASC
        """
        query_job = client.query(query)
        results = query_job.result()

        # Extract data
        years = []
        consumption = []
        for row in results:
            years.append(row["Year"])
            consumption.append(row["Renewable_Energy_Consumption"])

        if not years or not consumption:
            raise HTTPException(status_code=404, detail="No data found for the specified country")

        # Generate and save graph
        graph_path = os.path.join(GRAPH_FOLDER, f"{country_code}_renewable_energy.png")
        plt.figure(figsize=(10, 6))
        plt.plot(years, consumption, marker='o', linestyle='-', color='b')
        plt.title(f"Renewable Energy Consumption in {country_code}")
        plt.xlabel("Year")
        plt.ylabel("Renewable Energy Consumption (%)")
        plt.grid(True)
        plt.savefig(graph_path)
        plt.close()

        return FileResponse(graph_path, media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving graph for {country_code}: {str(e)}")
