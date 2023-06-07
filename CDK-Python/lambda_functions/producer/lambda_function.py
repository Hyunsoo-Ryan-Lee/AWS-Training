def lambda_handler(event, context):
    print("Hello from Producer")
    return {
        'statusCode': 200,
    }