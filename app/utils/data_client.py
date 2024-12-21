# app/utils/data_client.py

import os
from google.cloud import bigquery
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Authenticate with the service account key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

def fetch_climate_data():
    """
    Fetch climate data from BigQuery public dataset.
    
    Returns:
        List[Dict]: Climate data as a list of dictionaries.
    """
    client = bigquery.Client()

    query = """
        SELECT year, average_temperature, country
        FROM `global-environment-project.climate_data.global_temperature`
        ORDER BY year DESC
    """
    # Execute query
    query_job = client.query(query)
    # Collect results
    results = query_job.result()

    # Convert results to a list of dictionaries
    data = []
    for row in results:
        data.append({
            "year": row.year,
            "average_temperature": row.average_temperature,
            "country": row.country
        })
    return data

def fetch_data_from_bigquery(query: str):
    """
    Fetch data from BigQuery using a SQL query.
    
    Args:
        query (str): The SQL query to execute.
    
    Returns:
        List[Dict]: Query results as a list of dictionaries.
    """
    client = bigquery.Client()
    query_job = client.query(query)
    return [dict(row) for row in query_job.result()]
