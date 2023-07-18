import flet as ft
import uuid, ast
import requests
from pytz import timezone
from datetime import datetime
import random


currentTime = datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')

def main(page: ft.Page):
    page.title = "FastAPI Login With DynamoDB"
    page.bgcolor = "WHITE"
    page.scroll = "always"
    
    def snackBar(msg, color, time):
        page.snack_bar = ft.SnackBar(
                ft.Text(msg, size=17, weight=ft.FontWeight.BOLD),
                bgcolor=color,
                duration=time,
                )
        page.snack_bar.open = True
        page.update()
        
    def delete_textfield():
        name_field.value, email_field.value = "", ""
        
    def get_request(e):

        
        res = requests.get("http://127.0.0.1:5000/dynamo/")
        key_order = ["id", "name", 'email', 'time', 'ect']
        data = ast.literal_eval(res.text)
        vals = list({k : d_.get(k, 0) for k in key_order}.values() for d_ in data["data"])
        
        dataTable = ft.DataTable(

            columns=[ft.DataColumn(ft.Text(i)) for i in key_order],
            rows=[ft.DataRow(
                cells= [ft.DataCell(ft.Text(j, color="WHITE")) for j in i],
                color= "BLACK"
                ) for i in vals],
            bgcolor="BLUE"
        )
        
        page.controls.insert(4, dataTable)
        page.update()        

        
        
        

    def delete_request(e, name):
        res = requests.delete(f"http://127.0.0.1:5000/dynamo/{name}")
    
    def register_request(e, name, email):
        
        if not name or not email:
            snackBar("Please fill in the requirements", "RED", 1500)
        
        else:
            data = {
                "id": str(uuid.uuid1()),
                "time": str(currentTime),
                "name": name,
                "email": email,
                "ect": random.randint(1,1000)
            }
            res = requests.post("http://127.0.0.1:5000/dynamo/items/", json=data)
            try:
                if res.status_code == 200:
                    delete_textfield()
                    snackBar("Register Succeed!", "GREEN", 1500)
                    page.update()
            except Exception as e:
                print(e)
                snackBar("Something went wrong!", "RED", 1500)
                page.update()
    
    
    name_field = ft.TextField(
        label="name",
        border="underline",
        width=320,
        text_size=14,
        color='BLACK'
        # password=True,
        # can_reveal_password=True,
    )
    email_field = ft.TextField(
        label="Email",
        border="underline",
        width=320,
        text_size=14,
        color='BLACK'
    )
    get_field = ft.TextField(
        border="underline",
        width=320,
        text_size=14,
        color='BLACK'
    )
    delete_field = ft.TextField(
        label="delete name",
        # border="underline",
        width=100,
        text_size=14,
        color='BLACK'
    )
    
    delete_btn = ft.FilledButton(content=ft.Text("DEL", weight="w700")
                           , width=100
                           , height=40
                           , on_click=lambda e: delete_request(e, delete_field.value))
    
    btn1 = ft.FilledButton(content=ft.Text("Insert", weight="w700")
                           , width=140
                           , height=40
                           , icon_color= "green"
                           , on_click=lambda e: register_request(e, name_field.value, email_field.value)
                        #    , on_click=lambda e: to_lambda(e)
                           )

    btn2 = ft.FilledButton(content=ft.Text("Get", weight="w700")
                           , width=140
                           , height=40
                           , on_click=lambda e: get_request(e))
    
    
    
    
    page.add(
        ft.AppBar(title=ft.Text("Flet Login App"), bgcolor="blue")
        , ft.Column(controls=[name_field, email_field])
        , ft.Row(controls=[btn1, btn2])
        , ft.Divider(height=10, color='transparent')
        , get_field
        , ft.Divider(height=10, color='transparent')
        , ft.Row(controls=[delete_field, delete_btn])
    )
    
    
    
ft.app(target=main)