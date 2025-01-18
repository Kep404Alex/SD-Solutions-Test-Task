import pytest
from datetime import datetime
from unittest.mock import patch

@pytest.mark.asyncio
async def test_weather_endpoint_with_mock(client, dynamodb_mock):
    mock_weather_response = {
        "weather": [{"description": "clear sky"}],
        "main": {"temp": 293.15},
        "name": "London",
    }

    with patch("app.main.fetch_weather", return_value=mock_weather_response):
        city = "London"
        response = client.get(f"/weather?city={city}")
        assert response.status_code == 200
        assert response.json()["source"] in ["cache", "api"]
        assert response.json()["data"]["name"] == "London"
        assert response.json()["data"]["main"]["temp"] == 293.15


@pytest.mark.asyncio
async def test_logs_endpoint(client, dynamodb_mock):
    city = "London"
    timestamp = datetime.utcnow().isoformat()
    file_path = "/path/to/file"

    # Insert a test item into the mocked DynamoDB
    dynamodb_mock.put_item(
        TableName="WeatherLogs",
        Item={
            "city": {"S": city},
            "timestamp": {"S": timestamp},
            "file_path": {"S": file_path},
        },
    )

    # Test retrieving logs
    response = client.get(f"/logs?city={city}")
    assert response.status_code == 200
    logs = response.json()
    assert len(logs) == 1
    assert logs[0]["city"] == city
    assert logs[0]["timestamp"] == timestamp
    assert logs[0]["file_path"] == file_path


@pytest.mark.asyncio
async def test_weather_endpoint_with_invalid_city(client, dynamodb_mock):
    # Mock the fetch_weather function to return an error
    with patch("app.main.fetch_weather", return_value={"error": "City not found"}):
        city = "InvalidCity"
        response = client.get(f"/weather?city={city}")
        assert response.status_code == 400
        assert "detail" in response.json()
        assert response.json()["detail"] == "City not found"
