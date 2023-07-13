import flet as ft
from flet_route import Params, Basket
import requests



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
                "id": 1,
                "name": name,
                "email": email,
            }

            res = requests.post("http://127.0.0.1:5000/items/", json=data)
            if res.status_code == 200:
                delete_textfield()
                snackBar("Register Succeed!", "GREEN", 1500)
                page.update()
            else:
                snackBar("Something went wrong!", "RED", 1500)
                page.update()
            
    def settings_page(e):
        page.go("/settings")
    
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
                           , on_click=lambda e: register_request(e, name_field.value, email_field.value))

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