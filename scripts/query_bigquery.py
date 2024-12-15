from google.cloud import bigquery
import os

# Set environment variable for Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/gramm/Desktop/PythonStudying/global_environment_api/keyfile.json"

def query_bigquery():
    """
    Execute a SQL query on BigQuery and print results.
    """
    client = bigquery.Client()

    # SQL query (use correct column names)
    query = """
        SELECT *
        FROM `global-environment-project.renewable_energy_data.renewable_energy_consumption`
        WHERE `Country Code` = 'ABW'
        ORDER BY Year DESC;
    """

    # Execute query
    query_job = client.query(query)

    # Print results
    for row in query_job.result():
        print(f"Year: {row.Year}, Country: {row['Country Name']}, Renewable Energy Consumption: {row.Renewable_Energy_Consumption}")

if __name__ == "__main__":
    query_bigquery()
