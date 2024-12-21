import pytest
from app.utils.data_client import fetch_climate_data
from google.cloud import bigquery


@pytest.fixture
def mock_climate_query_results(monkeypatch):
    """
    Mock BigQuery query results for testing fetch_climate_data.
    """
    def mock_query(self, query, *args, **kwargs):
        class MockRow:
            def __init__(self, year, average_temperature, country):
                self.year = year
                self.average_temperature = average_temperature
                self.country = country

        class MockQueryJob:
            def result(self):
                return [
                    MockRow(2023, 15.5, "USA"),
                    MockRow(2022, 15.3, "USA"),
                ]

        return MockQueryJob()

    # Replace the BigQuery client's query method with the mock
    monkeypatch.setattr(bigquery.Client, "query", mock_query)


def test_fetch_climate_data_with_mock(mock_climate_query_results):
    """
    Test fetch_climate_data function with mock data.
    """
    # Call the function under test
    data = fetch_climate_data()

    # Verify the results
    assert len(data) == 2
    assert data[0]["year"] == 2023
    assert data[0]["average_temperature"] == 15.5
    assert data[0]["country"] == "USA"
    assert data[1]["year"] == 2022
    assert data[1]["average_temperature"] == 15.3
    assert data[1]["country"] == "USA"


@pytest.mark.skip(reason="This test requires a live BigQuery instance.")
def test_fetch_climate_data_actual():
    """
    Test fetch_climate_data function with actual BigQuery.
    """
    pass
