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

4. **High Performance**:
   - Built on **FastAPI** and powered by **Google BigQuery** for fast data querying.

5. **Renewable Energy Forecasting**:
   - Predict future renewable energy consumption trends based on historical data.
   - Generate detailed forecast charts with confidence intervals.
   - Example: `/energy/forecast/renewable-energy?country=USA&years=5`
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

#### Example Query:
```bash
curl -X GET "http://127.0.0.1:8000/energy/forecast/renewable-energy?country=USA&years=5"
```

#### Example Response:
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
│       └── data_client.py    # BigQuery client helper
├── static/                   
│   ├── graphs/               # Saved graph images
│   └── exports/              # Exported forecast data (e.g., CSV/Excel)
├── tests/                    
│   └── test_energy.py        # Unit tests
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
