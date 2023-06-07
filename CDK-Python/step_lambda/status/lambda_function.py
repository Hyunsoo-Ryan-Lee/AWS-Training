import json

def lambda_handler(event, context):
    if event["STATUS"] == "SUCCEEDED":
        return {"status": "SUCCEEDED"}
    else:
        return {"status": "FAILED"}