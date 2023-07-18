from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from dynamo_functions import get_all_data_from_dynamodb, insert_data_to_dynamodb, delete_records_by_name


app = FastAPI()

class Dynamo(BaseModel):
    id: str
    time: str
    name: str
    email: str
    ect: int

table_name = 'FastAPI_DB'
    
    
@app.get("/dynamo/")
def get_all_items():
    res = get_all_data_from_dynamodb(table_name)
    return {"data":res}

@app.post('/dynamo/items/')
def create_item(data: Dynamo):
    
    data = {
        'id': data.id, 
        "time": data.time, 
        'email': data.email, 
        'name': data.name,
        "ect": data.ect
        }
    res = insert_data_to_dynamodb(table_name, data)

    return {"response": res,
            "data" : data}
    
@app.delete('/dynamo/{item_name}')
def delete_item(item_name: str):
    res = delete_records_by_name(table_name, item_name)
    
    return {"response": res}
    
    
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)