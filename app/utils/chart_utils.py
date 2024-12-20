import matplotlib.pyplot as plt
from io import BytesIO

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
