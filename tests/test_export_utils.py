import os
from app.utils.export_utils import export_to_csv, export_to_excel, export_to_pdf

def test_export_to_csv():
    """Test exporting data to CSV."""
    data = [{"year": 2023, "consumption": 10.5}]
    file_name = "test_export.csv"
    file_path = export_to_csv(data, file_name)
    assert os.path.exists(file_path), "CSV file was not created"
    os.remove(file_path)

def test_export_to_excel():
    """Test exporting data to Excel."""
    data = [{"year": 2023, "consumption": 10.5}]
    file_name = "test_export.xlsx"
    file_path = export_to_excel(data, file_name)
    assert os.path.exists(file_path), "Excel file was not created"
    os.remove(file_path)

def test_export_to_pdf():
    """Test exporting data to PDF."""
    data = [{"year": 2023, "consumption": 10.5}]
    file_name = "test_export.pdf"
    file_path = export_to_pdf(data, file_name, "Test Report")
    assert os.path.exists(file_path), "PDF file was not created"
    os.remove(file_path)
