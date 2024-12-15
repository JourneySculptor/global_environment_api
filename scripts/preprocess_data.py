 # File: scripts/preprocess_data.py

import pandas as pd

def preprocess_data(input_file: str, output_file: str):
    """
    Preprocess the renewable energy consumption data.

    Args:
        input_file (str): Path to the raw CSV file.
        output_file (str): Path to save the cleaned data.

    Returns:
        None
    """
    # Load the raw data
    data = pd.read_csv(input_file, skiprows=4)

    # Select relevant columns (Country Name, Country Code, Years 2000-2021)
    columns_to_keep = ["Country Name", "Country Code"] + [str(year) for year in range(2000, 2022)]
    filtered_data = data[columns_to_keep]

    # Drop rows with missing values in key columns
    cleaned_data = filtered_data.dropna()

    # Save the processed data to the specified output file
    cleaned_data.to_csv(output_file, index=False)

    print(f"Preprocessed data saved to: {output_file}")


# Example usage
if __name__ == "__main__":
    preprocess_data(
        "data/raw/renewable_energy_consumption.csv",
        "data/processed/cleaned_energy_data.csv"
    )

