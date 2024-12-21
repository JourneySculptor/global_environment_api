# Global Environment API

This project provides a robust and scalable RESTful API for analyzing **climate data** and **renewable energy consumption trends**. Designed for environmental researchers, data analysts, and decision-makers, it enables querying, filtering, and visualization of global data with ease.

---

## **Features**

1. **Climate Data Filtering**:
   - Retrieve global temperature data by **year** and **country**.
   - Example: `/energy/climate-data?year=2020&country=USA`

2. **Renewable Energy Trends**:
   - Fetch renewable energy consumption data for any country and year.
   - Visualize energy trends with **bar charts, line graphs**.

3. **Graph Generation & Saving**:
   - Generate interactive graphs for energy data, including **forecast trends**.
   - Save graphs locally for reports or presentations.

4. **Detailed Report Generation**:
   - Export renewable energy forecast data as **CSV**, **Excel**, or **PDF** for further analysis or presentation.
   - Example: `/energy/export/forecast?country=USA&years=5&format=csv`

5. **Renewable Energy Forecasting**:
   - Predict future renewable energy consumption trends based on historical data.
   - Generate detailed forecast charts with confidence intervals.
   - Example: `/energy/forecast/renewable-energy?country=USA&years=5`

6. **Debugging Support**:
   - A new tool, `search_keywords.py`, helps developers locate specific terms in the codebase.
   - Example: Quickly identify files that reference specific functions or variables.

---

## **API Endpoints**

### **Climate Data**
| Method | Endpoint                   | Description                                      |
|--------|----------------------------|--------------------------------------------------|
| GET    | `/energy/climate-data`     | Fetch climate data (average temperature).        |
| GET    | `/energy/climate-data?year=2020` | Filter data by year.                          |
| GET    | `/energy/climate-data?country=USA` | Filter data by country.                     |
| GET    | `/energy/climate-data?year=2020&country=USA` | Combine filters for year and country. |
| GET    | `/energy/forecast/renewable-energy` | Predict future renewable energy consumption. |
| GET    | `/energy/export/forecast`                    | Export forecasted renewable energy data.        |

#### Example Query 1:
```bash
curl -X GET "http://127.0.0.1:8000/energy/forecast/renewable-energy?country=USA&years=5"
```

#### Example Response 1:
```json
{
  "status": "success",
  "data": [
    {"year": 2022, "predicted_consumption": 10.54},
    {"year": 2023, "predicted_consumption": 10.77},
    {"year": 2024, "predicted_consumption": 11.0},
    {"year": 2025, "predicted_consumption": 11.23},
    {"year": 2026, "predicted_consumption": 11.46}
  ],
  "graph_url": "/static/graphs/USA_forecast_chart.png"
}
```

#### Example Query 2:
```bash
curl -X GET "http://127.0.0.1:8000/energy/export/forecast?country=USA&years=5&format=csv"
```
#### Supported Formats:
- CSV
- Excel
- PDF

#### Example Response 2:
```json
{
  "status": "success",
  "file_url": "/static/exports/USA_forecast.csv"
}
```

---

## **Test Coverage**

This project has comprehensive unit tests to ensure reliability and accuracy. Current test coverage:

**Newly added tests**:
- Export functionality for CSV, Excel, and PDF.
- Validations for renewable energy forecast parameters.

```plaintext
---------- coverage: platform win32, python 3.12.4-final-0 -----------
Name                            Stmts   Miss  Cover
---------------------------------------------------
app\routers\energy.py             123      8    93%
app\routers\predictions.py         45      3    93%
app\utils\chart_utils.py           52     28    46%
app\utils\data_client.py           18      3    83%
app\utils\export_utils.py          47     18    62%
app\utils\report_utils.py          29      1    97%
---------------------------------------------------
TOTAL                             347     64    82%
```
**Note**: Ongoing efforts are being made to improve coverage, especially for utility functions like `export_utils.py` and `chart_utils.py`.

---

### **Renewable Energy Data**
| Method | Endpoint                                      | Description                                      |
|--------|----------------------------------------------|--------------------------------------------------|
| GET    | `/energy/renewable-energy/{country_code}`    | Fetch renewable energy consumption by country.   |
| GET    | `/energy/graph/bar/renewable-energy/{country_code}` | Generate a bar chart for energy trends.  |
| GET    | `/energy/graph/line/renewable-energy/{country_code}` | Generate a line chart for energy trends.  |


---

## **Graph Generation**

### **1. Display Graphs**
Generate graphs directly in the browser.

- **Example**:  
  - Bar Chart: `http://127.0.0.1:8000/energy/graph/bar/renewable-energy/JPN`  
  - Line Chart: `http://127.0.0.1:8000/energy/graph/line/renewable-energy/JPN`  

### **2. Save Graphs Locally**
Save generated graphs as PNG files to the `static/graphs/` folder.

- **Example**:  
  - `static/graphs/JPN_bar_chart.png`  
  - `static/graphs/JPN_line_chart.png`


---

## **Example Graphs**

### **Bar Chart: Renewable Energy in Japan**
![Japan Renewable Energy Bar Chart](static/graphs/JPN_bar_chart.png)

### **Line Chart: Renewable Energy in Japan**
![Japan Renewable Energy Line Chart](static/graphs/JPN_line_chart.png)

### **Forecast Chart: Renewable Energy in USA**
![USA Renewable Energy Forecast Chart](static/graphs/USA_forecast_chart.png)

### **Forecast Report: Renewable Energy in USA (CSV)**
![Forecast CSV](static/exports/USA_forecast_example.png)

### **Forecast Report: Renewable Energy in USA (Excel)**
![Forecast Excel](static/exports/USA_forecast_excel_example.png)

### **Forecast Report: Renewable Energy in USA (PDF)**
![Forecast PDF](static/exports/USA_forecast_pdf_example.png)

---

## **Getting Started**

### **Prerequisites**
- Python 3.10+
- Google Cloud SDK with BigQuery enabled.
- Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable.

### **Installation Steps**

1. Clone the repository:
   ```bash
   git clone https://github.com/JourneySculptor/global_environment_api.git
   cd global_environment_api
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set your Google service account key:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/keyfile.json"
   ```

4. Run the server locally:
   ```bash
   uvicorn app.api_server:app --reload
   ```

5. Test the API:
   ```bash
   curl -X GET "http://127.0.0.1:8000/energy/climate-data"
   ```

6. Use the Debugging Tool: If you need to locate specific terms or references in the codebase, you can use the debugging tool:
   ```bash
   python search_keywords.py
   ```
This tool helps identify files where specific keywords or functions are referenced.

---

## **Folder Structure**

```plaintext
global_environment_api/
├── app/
│   ├── api_server.py         # FastAPI application
│   ├── routers/
│   │   ├── energy.py         # API endpoints for energy data
│   │   └── predictions.py    # API endpoints for forecasts
│   ├── utils/
│       ├── chart_utils.py    # Functions for graph generation
│       ├── prediction_utils.py # Functions for forecast calculations
│       ├── export_utils.py   # Functions for exporting forecast data
│       ├── data_client.py    # BigQuery client helper
│       └── report_utils.py   # Functions for generating reports
├── static/
│   ├── graphs/               # Saved graph images
│   └── exports/              # Exported forecast data (e.g., CSV/Excel/PDF)
├── tests/
│   ├── test_energy.py        # Unit tests for energy endpoints
│   ├── test_predictions.py   # Unit tests for prediction endpoints
│   ├── test_export_utils.py  # Unit tests for export utilities
│   ├── test_data_client.py   # Unit tests for BigQuery client helper
├── search_keywords.py        # Script for searching keywords in the project
├── requirements.txt          # Dependencies
├── Dockerfile                # Docker setup
├── .env                      # Environment variables
└── README.md                 # Project documentation
```

---

## **Future Enhancements**
- **Geospatial Analysis**: Introduce geographic data visualizations for renewable energy trends.
- **Confidence Intervals**: Improve forecast accuracy with detailed statistical models.
- **Enhanced Data Sources**: Continuously update with the latest global energy data.

---

## **License**
This project is licensed under the MIT License.
