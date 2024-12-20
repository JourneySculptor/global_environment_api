import os
import pandas as pd
from fastapi import HTTPException

EXPORT_FOLDER = "static/exports"

if not os.path.exists(EXPORT_FOLDER):
    os.makedirs(EXPORT_FOLDER)

def export_data(df: pd.DataFrame, filename: str, format: str):
    """
    Export data to the specified format (CSV or Excel).
    """
    file_path = os.path.join(EXPORT_FOLDER, filename)

    if format.lower() == "csv":
        df.to_csv(file_path, index=False)
        content_type = "text/csv"
    elif format.lower() == "excel":
        df.to_excel(file_path, index=False, engine="openpyxl")
        content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    else:
        raise HTTPException(status_code=400, detail="Invalid format. Use 'csv' or 'excel'.")

    return file_path, content_type
