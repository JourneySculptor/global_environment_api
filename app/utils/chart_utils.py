import os
import matplotlib.pyplot as plt
from io import BytesIO
import logging

# Set up logger
logger = logging.getLogger(__name__)

# Directory for saving graphs
GRAPH_FOLDER = "static/graphs"
if not os.path.exists(GRAPH_FOLDER):
    os.makedirs(GRAPH_FOLDER)

def save_chart_and_return_path(buf, filename: str):
    """
    Save the chart buffer to a file and return the file path.

    Args:
        buf (BytesIO): Chart data in memory buffer.
        filename (str): File name to save.

    Returns:
        str: File path where the chart is saved.
    """
    file_path = os.path.join(GRAPH_FOLDER, filename).replace("\\", "/")  # Ensure proper path format
    with open(file_path, "wb") as f:
        f.write(buf.getvalue())
    logger.info(f"Chart saved at: {file_path}")
    return file_path

def generate_bar_chart(x_values, y_values, title: str, x_label: str, y_label: str):
    """Generate a bar chart."""
    plt.figure(figsize=(12, 7))
    plt.bar(x_values, y_values, color='skyblue')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xticks(rotation=45)
    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return buf

def generate_line_chart(x_values, y_values, title: str, x_label: str, y_label: str):
    """Generate a line chart."""
    plt.figure(figsize=(12, 7))
    plt.plot(x_values, y_values, marker='o', linestyle='-', color='b')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xticks(rotation=45)
    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return buf

def generate_forecast_line_chart(
    past_years, past_values, future_years, future_values, title: str, x_label: str, y_label: str
):
    """
    Generate a line chart for past and forecast data with legends.
    """
    plt.figure(figsize=(12, 7))
    plt.plot(past_years, past_values, marker='o', linestyle='-', color='b', label='Past Data')
    plt.plot(future_years, future_values, marker='o', linestyle='--', color='r', label='Forecast Data')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xticks(rotation=45)
    plt.legend()
    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return buf
