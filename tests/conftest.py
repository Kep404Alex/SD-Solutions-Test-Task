from unittest.mock import patch

import boto3
import pytest
from fastapi.testclient import TestClient
from moto import mock_aws

from app.db import TABLE_NAME
from app.main import app

DYNAMODB_ENDPOINT = "http://localhost:8001"
@pytest.fixture(scope="function")
def dynamodb_mock():
    """Mock DynamoDB for testing."""
    with mock_aws():
        dynamodb = boto3.client(
            "dynamodb",
            region_name="us-east-1",
            aws_access_key_id="dummy",  # Dummy credentials
            aws_secret_access_key="dummy",  # Dummy credentials
        )
        dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {"AttributeName": "city", "KeyType": "HASH"},  # Partition key
                {"AttributeName": "timestamp", "KeyType": "RANGE"},  # Sort key
            ],
            AttributeDefinitions=[
                {"AttributeName": "city", "AttributeType": "S"},
                {"AttributeName": "timestamp", "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
        )
        yield dynamodb


def mock_get_dynamodb_client():
    dynamodb = boto3.client(
    "dynamodb",
    region_name="us-east-1",
    aws_access_key_id="dummy",  # Dummy credentials
    aws_secret_access_key="dummy",  # Dummy credentials
    )
    return dynamodb

@pytest.fixture(scope="module")
def client():
    with patch("app.db.get_dynamodb_client", mock_get_dynamodb_client):
        with TestClient(app) as test_client:
            yield test_client
