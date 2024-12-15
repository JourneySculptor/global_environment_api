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