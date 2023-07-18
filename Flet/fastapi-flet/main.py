from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
from typing import List
import mysql.connector


import boto3
import uuid
from pytz import timezone
from datetime import datetime
currentTime = datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')
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

def insert_data_to_dynamodb(table_name, data):
    dynamodb = boto3.resource('dynamodb')

    try:
        table = dynamodb.Table(table_name)
        response = table.put_item(Item=data)
        return True

    except Exception as e:
        print(f"Error inserting data into DynamoDB: {e}")
        return False

# Define the FastAPI app
app = FastAPI()

# Define a model for your data
class Item(BaseModel):
    id: int
    name: str
    email: str

class Dynamo(BaseModel):
    id: str
    time: str
    name: str
    email: str

# Create a MySQL connection pool
db_connection = mysql.connector.connect(
        host="localhost",
        user="hyunsoo",
        password="150808",
        database="flet"
        )
db_cursor = db_connection.cursor(buffered=True)

# API endpoints

@app.get('/dynamo/')
def get_dynamo():
    res = get_all_data_from_dynamodb(table_name)
    return {"data":res}

@app.post('/dynamo/items/')
def create_item(data: Dynamo):
    
    data = {'id': data.id, 
            "time": data.time, 
            'email': data.email, 
            'name': data.name}
    
    res = insert_data_to_dynamodb(table_name, data)
    print(res)
    return {"response": res,
            "data" : data}
    
@app.get('/items/', response_model=List[Item])
def get_items():
    db_cursor.execute('SELECT * FROM items')
    items = []
    for (id, name, email) in db_cursor:
        items.append({'id': id, 'name': name, 'email': email})
    return items

@app.get('/items/{item_id}', response_model=Item)
def get_item(item_id: int):
    db_cursor.execute('SELECT * FROM items WHERE id = %s', (item_id,))
    row = db_cursor.fetchone()
    if row:
        return {'id': row[0], 'name': row[1], 'email': row[2]}
    else:
        raise HTTPException(status_code=404, detail='Item not found')

@app.post('/items/', response_model=Item)
def create_item(item: Item):
    print(item)
    db_cursor.execute('INSERT INTO items (id, name, email) VALUES (%s, %s, %s)',
                    (item.id, item.name, item.email))
    db_connection.commit()
    item.id = db_cursor.lastrowid

    return item

@app.put('/items/{item_id}', response_model=Item)
def update_item(item_id: int, item: Item):
    db_cursor.execute('UPDATE items SET name = %s, email = %s WHERE id = %s',
                      (item.name, item.email, item_id))
    db_connection.commit()
    return item

@app.delete('/items/{item_id}')
def delete_item(item_id: int):
    db_cursor.execute('DELETE FROM items WHERE id = %s', (item_id,))
    db_connection.commit()
    return {'message': 'Item deleted'}

# Close the database connection on shutdown
@app.on_event('shutdown')
def shutdown_event():
    db_connection.close()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
