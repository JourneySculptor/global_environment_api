from google.cloud import bigquery
from app.utils.prediction_utils import calculate_forecast
from app.utils.chart_utils import generate_forecast_line_chart
from app.utils.report_utils import export_to_csv, export_to_excel, export_to_pdf
from fastapi.responses import FileResponse
from fastapi import APIRouter, HTTPException, Query
import pandas as pd
import os


# Initialize BigQuery client
client = bigquery.Client()

router = APIRouter()


@router.get("/energy/forecast/renewable-energy")
async def forecast_renewable_energy(
    country: str = Query(..., description="Country code to filter data"),
    years: int = Query(5, description="Number of years to forecast")
):
    """
    Forecast future renewable energy consumption with confidence intervals.

    Args:
        country (str): Country code to filter data.
        years (int): Number of years to forecast.

    Returns:
        JSON: Forecast data and graph URL.
    """
    # Validate the years parameter
    if years > 50:
        raise HTTPException(status_code=400, detail="Years parameter exceeds allowed range.")

    # Query to fetch historical renewable energy consumption data
    query = f"""
        SELECT Year AS year, Renewable_Energy_Consumption AS consumption
        FROM `global-environment-project.renewable_energy_data.renewable_energy_consumption`
        WHERE `Country Code` = '{country}'
        ORDER BY Year ASC
    """


    # Fetch data from BigQuery
    try:
        query_job = client.query(query)
        results = query_job.result()
        data = [{"year": row["year"], "consumption": row["consumption"]} for row in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data from BigQuery: {str(e)}")

    # Check if data exists
    if not data:
        raise HTTPException(status_code=404, detail="No data found for the given country.")

    # Convert data to DataFrame
    df = pd.DataFrame(data)


    # Perform forecast calculations
    future_years, predictions = calculate_forecast(df, years)

    # Generate a forecast graph
    buf = generate_forecast_line_chart(
        past_years=list(df["year"]),
        past_values=list(df["consumption"]),
        future_years=list(future_years),
        future_values=list(predictions),
        title=f"Renewable Energy Forecast for {country}",
        x_label="Year",
        y_label="Consumption (%)"
    )

    # Save the chart as a PNG file
    filename = f"{country}_forecast_chart.png"
    file_path = f"static/graphs/{filename}"
    with open(file_path, "wb") as f:
        f.write(buf.getbuffer())

    # Return forecast data and graph URL
    return {
        "status": "success",
        "data": [{"year": int(y), "predicted_consumption": round(p, 2)}
                 for y, p in zip(future_years, predictions)],
        "graph_url": f"/{file_path}"
    }


@router.get("/energy/export/forecast")
async def export_forecast_data(
    country: str = Query(..., description="Country code to filter data"),
    years: int = Query(5, description="Number of years to forecast"),
    format: str = Query("csv", description="File format: 'csv', 'excel', or 'pdf'")
):
    """
    Export forecasted renewable energy data as CSV, Excel, or PDF.

    Args:
        country (str): Country code to filter data.
        years (int): Number of years to forecast.
        format (str): Desired file format ('csv', 'excel', or 'pdf').

    Returns:
        FileResponse: The exported file.
    """
    # Simulated forecast data (Replace with actual calculation logic)
    forecast_data = [
        {"year": 2023, "predicted_consumption": 10.54},
        {"year": 2024, "predicted_consumption": 10.77},
        {"year": 2025, "predicted_consumption": 11.0},
        {"year": 2026, "predicted_consumption": 11.23},
        {"year": 2027, "predicted_consumption": 11.46},
    ]

    if format.lower() == "csv":
        file_path = export_to_csv(forecast_data, f"{country}_forecast.csv")
        media_type = "text/csv"
    elif format.lower() == "excel":
        file_path = export_to_excel(forecast_data, f"{country}_forecast.xlsx")
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    elif format.lower() == "pdf":
        file_path = export_to_pdf(forecast_data, f"{country}_forecast.pdf", f"Forecast for {country}")
        media_type = "application/pdf"
    else:
        raise HTTPException(status_code=400, detail="Invalid format. Use 'csv', 'excel', or 'pdf'.")

    return FileResponse(
        file_path,
        media_type=media_type,
        filename=os.path.basename(file_path)
    )

