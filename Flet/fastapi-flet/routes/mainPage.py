import flet as ft
from flet_route import Params, Basket
import requests
import uuid
import json
from pytz import timezone
from datetime import datetime

currentTime = datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')


def mainPageView(page: ft.Page, params: Params, basket: Basket):

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
    
    def register_request(e, name, email):
        
        if not name or not email:
            snackBar("Please fill in the requirements", "RED", 1500)
        
        else:
            data = {
                "id": str(uuid.uuid1()),
                "time": str(currentTime),
                "name": name,
                "email": email
            }
            print(data)
            # res = requests.post("http://127.0.0.1:5000/items/", json=data)
            # res = requests.post("http://127.0.0.1:5000/dynamo/items/", json=data)
            res = requests.post("https://2qkgncc2cu3g4rypjspqezm4mq0wbpdc.lambda-url.ap-northeast-2.on.aws/dynamo/items/"
                                , json=data
                                , allow_redirects=False)
            print(res.text)
            try:
                if res.status_code == 200:
                    delete_textfield()
                    snackBar("Register Succeed!", "GREEN", 1500)
                    page.update()
            except Exception as e:
                print(e)
                snackBar("Something went wrong!", "RED", 1500)
                page.update()
            
    def settings_page(e):
        page.go("/settings")
        
    def to_lambda(e):
        data = {
            "id": uuid.uuid1(),
            "time": currentTime,
            "name": "name",
            "email": "email",
        }
        # res = requests.get("https://2qkgncc2cu3g4rypjspqezm4mq0wbpdc.lambda-url.ap-northeast-2.on.aws/", json={})
        res = requests.post("https://2qkgncc2cu3g4rypjspqezm4mq0wbpdc.lambda-url.ap-northeast-2.on.aws/items/", json={})
        print(res.text)
    
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
    
    btn1 = ft.FilledButton(content=ft.Text("Login", weight="w700")
                           , width=140
                           , height=40
                           , icon_color= "green"
                           , on_click=lambda e: register_request(e, name_field.value, email_field.value)
                        #    , on_click=lambda e: to_lambda(e)
                           )

    btn2 = ft.FilledButton(content=ft.Text("Register", weight="w700")
                           , width=140
                           , height=40
                           , on_click=settings_page)
    
    return ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Flet app"))
                    , ft.Column(controls=[name_field, email_field])
                    , ft.Row(controls=[btn1, btn2])
                ],
            )