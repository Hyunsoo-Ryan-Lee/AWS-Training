import boto3

def get_all_data_from_dynamodb(table_name):
    dynamodb = boto3.resource('dynamodb')

    try:
        table = dynamodb.Table(table_name)
        response = table.scan()
        items = response['Items']
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response['Items'])

        return items

    except Exception as e:
        print(f"Error retrieving data from DynamoDB: {e}")
        return []

def insert_data_to_dynamodb(table_name, data):
    dynamodb = boto3.resource('dynamodb')

    try:
        table = dynamodb.Table(table_name)
        response = table.put_item(Item=data)
        return True

    except Exception as e:
        print(f"Error inserting data into DynamoDB: {e}")
        return False
    
    
import boto3

def delete_records_by_name(table_name, name):
    dynamodb = boto3.resource('dynamodb')

    try:
        table = dynamodb.Table(table_name)
        response = table.scan(FilterExpression=boto3.dynamodb.conditions.Attr('name').eq(name))
        items = response['Items']

        with table.batch_writer() as batch:
            for item in items:
                batch.delete_item(Key={'id': item['id']})

        return True

    except Exception as e:
        print(f"Error deleting records from DynamoDB: {e}")
        return False
