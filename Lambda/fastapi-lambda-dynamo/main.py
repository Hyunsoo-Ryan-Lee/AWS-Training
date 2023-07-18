from fastapi import FastAPI
from mangum import Mangum
import boto3
# from pytz import timezone
from datetime import datetime
from pydantic import BaseModel

app = FastAPI()
handler = Mangum(app)

class Dynamo(BaseModel):
    id: str
    time: str
    name: str
    email: str

# currentTime = datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')
table_name = 'FastAPI_DB'

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
    

# def insert_data_to_dynamodb(table_name, data):
#     dynamodb = boto3.resource('dynamodb')

#     try:
#         table = dynamodb.Table(table_name)
#         response = table.put_item(Item=data)
#         return True

#     except Exception as e:
#         print(f"Error inserting data into DynamoDB: {e}")
#         return False

@app.get("/")
def home():
    return {"message":"hello!"}

@app.get('/dynamo/', )
def get_dynamo():
    res = get_all_data_from_dynamodb(table_name)
    return {"data":res}

# @app.post('/dynamo/items/')
# def create_item(data: Dynamo):
    
#     data = {'id': data.id, 
#             "time": data.time, 
#             'email': data.email, 
#             'name': data.name}
    
#     res = insert_data_to_dynamodb(table_name, data)
#     print(res)
#     return {"response": res,
#             "data" : data}

# if __name__ == "__main__":
#     res = get_all_data_from_dynamodb(table_name)
#     print(res)
