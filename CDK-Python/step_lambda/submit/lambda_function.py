import json


def lambda_handler(event, context):
    print("Hello from SUBMIT")
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Hello from SUBMIT"}),
    }
