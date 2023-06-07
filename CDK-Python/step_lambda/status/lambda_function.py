import json


def lambda_handler(event, context):
    print("Hello from STATUS")
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Hello from STATUS"}),
    }
