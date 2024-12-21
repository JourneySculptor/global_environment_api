import os
import pandas as pd
from fastapi import HTTPException
from fpdf import FPDF

EXPORT_FOLDER = "static/exports"

if not os.path.exists(EXPORT_FOLDER):
    os.makedirs(EXPORT_FOLDER)

def export_data(df: pd.DataFrame, filename: str, format: str):
    """
    Export data to the specified format (CSV, Excel, or PDF).
    """
    file_path = os.path.join(EXPORT_FOLDER, filename)

    if format.lower() == "csv":
        df.to_csv(file_path, index=False)
        content_type = "text/csv"
    elif format.lower() == "excel":
        df.to_excel(file_path, index=False, engine="openpyxl")
        content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    elif format.lower() == "pdf":
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for index, row in df.iterrows():
            pdf.cell(200, 10, txt=str(row.to_dict()), ln=True)
        pdf.output(file_path)
        content_type = "application/pdf"
    else:
        raise HTTPException(status_code=400, detail="Invalid format. Use 'csv', 'excel', or 'pdf'.")

    return file_path, content_type

def export_to_csv(data, filename):
    """
    Export data to a CSV file.
    """
    file_path = os.path.join(EXPORT_FOLDER, filename)
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)
    return file_path

def export_to_excel(data, filename):
    """
    Export data to an Excel file.
    """
    file_path = os.path.join(EXPORT_FOLDER, filename)
    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False, engine="openpyxl")
    return file_path

def export_to_pdf(data, filename, title):
    """
    Export data to a PDF file.
    """
    file_path = os.path.join(EXPORT_FOLDER, filename)
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=title, ln=True, align="C")
    pdf.ln(10)
    for record in data:
        pdf.cell(200, 10, txt=str(record), ln=True)
    pdf.output(file_path)
    return file_path

