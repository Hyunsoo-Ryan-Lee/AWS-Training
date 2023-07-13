from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
from typing import List
import mysql.connector

# Define the FastAPI app
app = FastAPI()

# Define a model for your data
class Item(BaseModel):
    id: int
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
