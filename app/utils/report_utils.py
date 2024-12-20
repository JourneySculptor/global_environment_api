import pandas as pd
from fpdf import FPDF
import os

EXPORT_FOLDER = "static/exports"

# Ensure the folder exists
if not os.path.exists(EXPORT_FOLDER):
    os.makedirs(EXPORT_FOLDER)

def export_to_csv(data: list, filename: str) -> str:
    """
    Export data to a CSV file.

    Args:
        data (list): List of dictionaries containing the data.
        filename (str): Name of the CSV file.

    Returns:
        str: Path to the saved CSV file.
    """
    file_path = os.path.join(EXPORT_FOLDER, filename)
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)
    return file_path

def export_to_excel(data: list, filename: str) -> str:
    """
    Export data to an Excel file.

    Args:
        data (list): List of dictionaries containing the data.
        filename (str): Name of the Excel file.

    Returns:
        str: Path to the saved Excel file.
    """
    file_path = os.path.join(EXPORT_FOLDER, filename)
    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False, engine="openpyxl")
    return file_path

def export_to_pdf(data: list, filename: str, title: str) -> str:
    """
    Export data to a PDF file.

    Args:
        data (list): List of dictionaries containing the data.
        filename (str): Name of the PDF file.
        title (str): Title of the PDF.

    Returns:
        str: Path to the saved PDF file.
    """
    file_path = os.path.join(EXPORT_FOLDER, filename)
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Title
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, txt=title, ln=True, align='C')

    # Table
    pdf.set_font("Arial", size=12)
    for idx, item in enumerate(data, start=1):
        pdf.cell(0, 10, txt=f"{idx}. " + ", ".join(f"{k}: {v}" for k, v in item.items()), ln=True)

    pdf.output(file_path)
    return file_path
