from fastapi import APIRouter, HTTPException
from google.cloud import bigquery

# Initialize BigQuery client once at module level
client = bigquery.Client()

router = APIRouter()

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
