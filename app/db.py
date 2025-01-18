import boto3
from botocore.exceptions import ClientError
from datetime import datetime
import asyncio

DYNAMODB_ENDPOINT = "http://dynamodb-local:8000"
TABLE_NAME = "WeatherLogs"

def get_dynamodb_client():
    dynamodb = boto3.client(
    "dynamodb",
    endpoint_url=DYNAMODB_ENDPOINT,
    region_name="us-east-1",
    aws_access_key_id="dummy",  # Dummy credentials
    aws_secret_access_key="dummy",  # Dummy credentials
    )
    return dynamodb

async def initialize_database():
    """Create the table if it doesn't already exist."""
    dynamodb = get_dynamodb_client()
    try:
        existing_tables = await asyncio.to_thread(dynamodb.list_tables)
        if TABLE_NAME not in existing_tables["TableNames"]:
            await asyncio.to_thread(
                dynamodb.create_table,
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
    except ClientError as e:
        print(f"Error initializing database: {e}")


async def add_weather_log(city: str, timestamp: datetime, file_path: str):
    """Add a log entry to DynamoDB."""
    dynamodb = get_dynamodb_client()

    try:
        await asyncio.to_thread(
            dynamodb.put_item,
            TableName=TABLE_NAME,
            Item={
                "city": {"S": city},
                "timestamp": {"S": timestamp.isoformat()},
                "file_path": {"S": file_path},
            },
        )
    except ClientError as e:
        print(f"Error adding weather log: {e}")


async def get_weather_logs(city: str):
    """Retrieve logs for a specific city."""
    dynamodb = get_dynamodb_client()

    try:
        response = await asyncio.to_thread(
            dynamodb.query,
            TableName=TABLE_NAME,
            KeyConditionExpression="city = :city",
            ExpressionAttributeValues={":city": {"S": city}},
        )
        items = response.get("Items", [])
        return [
            {
                "city": item["city"]["S"],
                "timestamp": item["timestamp"]["S"],
                "file_path": item["file_path"]["S"],
            }
            for item in items
        ]
    except ClientError as e:
        print(f"Error retrieving weather logs: {e}")
        return []
