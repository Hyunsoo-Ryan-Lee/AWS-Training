import flet as ft
from flet_route import Routing, path
from routes.mainPage import mainPageView
from routes.registerPage import registerPageView
from routes.tempPage import tempPageView

def main(page: ft.Page):
    page.title = "FastAPI Login Page"
    page.bgcolor = ft.colors.AMBER
    page.scroll = "always"
    
    app_routes = [
        path(url='/', clear=True, view=mainPageView),
        path(url='/settings', clear=False, view=registerPageView),
        path(url='/temp', clear=False, view=tempPageView),
    ]
    
    Routing(page=page, app_routes=app_routes)
    
    page.go(page.route)
    page.update()
    
ft.app(target=main
       , name = ''
       , view = None
       , port = 2220
       )
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # def delete_textfield():
    #     name.value, email.value = "", ""
        
    # def snackBar(msg, color, time):
    #     page.snack_bar = ft.SnackBar(
    #             ft.Text(msg, size=17, weight=ft.FontWeight.BOLD),
    #             bgcolor=color,
    #             duration=time,
    #             )
    #     page.snack_bar.open = True
    #     page.update()

    # def register_request(e, name, email):
        
    #     if not name or not email:
    #         snackBar("Please fill in the requirements", "RED", 1500)
        
    #     else:
    #         data = {
    #             "id": 1,
    #             "name": name,
    #             "email": email,
    #         }

    #         # here, we call a POST request and route our data to the server URL and at the same time we pass in our data
    #         res = requests.post("http://127.0.0.1:5000/items/", json=data)
    #         if res.status_code == 200:
    #             delete_textfield()
    #             snackBar("Register Succeed!", "GREEN", 1500)
    #             page.update()
    #         else:
    #             snackBar("Something went wrong!", "RED", 1500)
    #             page.update()
            
    # def another_page(e):
    #     page.go("/settings")
    

    # name = ft.TextField(
    #     label="name",
    #     border="underline",
    #     width=320,
    #     text_size=14,
    #     color='BLACK'
    #     # password=True,
    #     # can_reveal_password=True,
    # )
    # email = ft.TextField(
    #     label="Email",
    #     border="underline",
    #     width=320,
    #     text_size=14,
    #     color='BLACK'
    # )

    # btn1 = ft.FilledButton(content=ft.Text("Login", weight="w700")
    #                        , width=140
    #                        , height=40
    #                        , icon_color= "green"
    #                        , on_click=lambda e: register_request(e, name.value, email.value))

    # btn2 = ft.FilledButton(content=ft.Text("Register", weight="w700")
    #                        , width=140
    #                        , height=40
    #                        , on_click=another_page)

    # def route_change(e):
    #     print("Route change:", e.route)
    #     page.views.clear()
    #     page.views.append(
    #         ft.View(
    #             "/",
    #             [
    #                 ft.AppBar(title=ft.Text("Flet app"))
    #                 , ft.Column(controls=[name, email])
    #                 , ft.Row(controls=[btn1, btn2])
    #             ],
    #         )
    #     )
    #     if page.route == "/settings":
    #         page.views.append(
    #             ft.View(
    #                 "/settings",
    #                 [
    #                     ft.AppBar(title=ft.Text("Settings"), bgcolor=ft.colors.SURFACE_VARIANT),
    #                     ft.Text("Settings!", style="bodyMedium"),
    #                     ft.ElevatedButton(
    #                         "Go to mail settings"
    #                     ),
    #                 ],
    #             )
    #         )
    #     page.update()
        
    # page.on_route_change = route_change


    # def view_pop(e):
    #     print("View pop:", e.view)
    #     page.views.pop()
    #     top_view = page.views[-1]
    #     page.go(top_view.route)
        
    # page.on_view_pop = view_pop