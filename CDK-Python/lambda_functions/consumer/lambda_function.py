def lambda_handler(event, context):
    print("Hello from Consumer")
    return {
        'statusCode': 200,
    }