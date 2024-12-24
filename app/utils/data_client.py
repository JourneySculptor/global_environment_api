import os
from google.cloud import bigquery
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ensure GOOGLE_APPLICATION_CREDENTIALS is set and valid
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not credentials_path:
    # Raise an error if the credentials are not set
    raise EnvironmentError("GOOGLE_APPLICATION_CREDENTIALS is not set in .env or invalid.")

# Explicitly set the environment variable for Google Application Credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

def fetch_climate_data():
    """
    Fetch climate data from BigQuery public dataset.
    
    Returns:
        List[Dict]: Climate data as a list of dictionaries.
    """
    try:
        # Initialize BigQuery client
        client = bigquery.Client()

        # Query to fetch climate data
        query = """
            SELECT year, average_temperature, country
            FROM `global-environment-project.climate_data.global_temperature`
            ORDER BY year DESC
        """

        # Execute query and collect results
        query_job = client.query(query)
        return [
            {"year": row.year, "average_temperature": row.average_temperature, "country": row.country}
            for row in query_job.result()
        ]
    except Exception as e:
        # Raise an error with details if fetching data fails
        raise RuntimeError(f"Error fetching climate data: {str(e)}")

def fetch_data_from_bigquery(query: str):
    """
    Fetch data from BigQuery using a SQL query.
    
    Args:
        query (str): The SQL query to execute.
    
    Returns:
        List[Dict]: Query results as a list of dictionaries.
    """
    try:
        # Initialize BigQuery client
        client = bigquery.Client()

        # Execute query and collect results
        query_job = client.query(query)
        return [dict(row) for row in query_job.result()]
    except Exception as e:
        # Raise an error with details if executing query fails
        raise RuntimeError(f"Error executing query: {str(e)}")
