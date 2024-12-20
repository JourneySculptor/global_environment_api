from sklearn.linear_model import LinearRegression 
import pandas as pd
import numpy as np

def calculate_forecast(df: pd.DataFrame, years: int):
    """
    Calculate forecast using a linear regression model.

    Args:
        df (pd.DataFrame): DataFrame containing past data with 'year' and 'consumption' columns.
        years (int): Number of years to forecast.

    Returns:
        tuple: (future_years, predictions)
    """
    # Debug: Log the input data
    print("Debug - Input DataFrame:\n", df.head())

    # Prepare the data for linear regression
    X = df["year"].values.reshape(-1, 1)  # Input: years
    y = df["consumption"].values          # Output: consumption

    # Train the linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # Generate future years starting from the latest year in the data
    last_year = df["year"].max()
    print("Debug - Last Year in Data:", last_year)  # Debug log

    future_years = np.arange(last_year + 1, last_year + 1 + years).reshape(-1, 1)

    # Predict future values
    predictions = model.predict(future_years)

    return future_years.flatten(), predictions
