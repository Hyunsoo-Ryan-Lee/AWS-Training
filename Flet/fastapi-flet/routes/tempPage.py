import flet as ft
from flet_route import Params, Basket



def tempPageView(page: ft.Page, params: Params, basket: Basket):

    def snackBar(msg, color, time):
        page.snack_bar = ft.SnackBar(
                ft.Text(msg, size=17, weight=ft.FontWeight.BOLD),
                bgcolor=color,
                duration=time,
                )
        page.snack_bar.open = True
        page.update()
        
    def to_home(e):
        page.go("/")
        
    return ft.View(
                    "/temp",
                    [
                        ft.AppBar(title=ft.Text("Temp"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.Text("Temp View!", style="bodyMedium"),
                        ft.ElevatedButton(
                            "Go to HOME"
                            , on_click=to_home
                        ),
                    ],
                )