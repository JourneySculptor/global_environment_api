import pandas as pd
import os
from google.cloud import bigquery

# Set environment variable for Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/gramm/Desktop/PythonStudying/global_environment_api/keyfile.json"

# BigQuery configuration
PROJECT_ID = "global-environment-project"
DATASET_ID = "renewable_energy_data"
TABLE_ID = "renewable_energy_consumption"

csv_file = "data/processed/cleaned_energy_data_long.csv"

data = pd.read_csv(csv_file)
print(data.columns)

def preprocess_data_wide_to_long(input_file: str, output_file: str):
    """
    Preprocess data from wide format to long format.

    Args:
        input_file (str): Path to the raw CSV file.
        output_file (str): Path to save the cleaned long format data.

    Returns:
        None
    """
    try:
        # Load the data and skip metadata rows
        data = pd.read_csv(input_file, skiprows=4)

        # Ensure only numeric year columns are selected
        year_columns = [col for col in data.columns if col.isdigit()]
        required_columns = ["Country Name", "Country Code"] + year_columns
        data = data[required_columns]

        # Convert wide format to long format
        long_format_data = pd.melt(
            data,
            id_vars=["Country Name", "Country Code"],
            var_name="Year",
            value_name="Renewable_Energy_Consumption"
        )

        # Ensure 'Year' is numeric and drop invalid rows
        long_format_data = long_format_data[long_format_data["Year"].str.isdigit()]
        long_format_data["Year"] = long_format_data["Year"].astype(int)

        # Drop rows with missing values
        cleaned_data = long_format_data.dropna()

        # Save the processed data
        cleaned_data.to_csv(output_file, index=False)
        print(f"Processed long format data saved to: {output_file}")
    except Exception as e:
        print(f"Error during preprocessing: {e}")

def upload_to_bigquery(csv_file):
    """
    Uploads a CSV file to BigQuery.

    Args:
        csv_file (str): Path to the CSV file to upload.
    """
    client = bigquery.Client()

    # Define table schema
    job_config = bigquery.LoadJobConfig(
    schema=[
        bigquery.SchemaField("Country Name", "STRING"),
        bigquery.SchemaField("Country Code", "STRING"),
        bigquery.SchemaField("Year", "INTEGER"),
        bigquery.SchemaField("Renewable_Energy_Consumption", "FLOAT"),
    ],
    skip_leading_rows=1,
    source_format=bigquery.SourceFormat.CSV,
)

    # Define full table ID
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    # Upload data to BigQuery
    with open(csv_file, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_ref, job_config=job_config)

    job.result()
    print(f"Uploaded {csv_file} to {table_ref}")

if __name__ == "__main__":
    # Preprocess data
    preprocess_data_wide_to_long(
        "data/raw/renewable_energy_consumption.csv",
        "data/processed/cleaned_energy_data_long.csv"
    )

    # Upload processed data to BigQuery
    upload_to_bigquery("data/processed/cleaned_energy_data_long.csv")
