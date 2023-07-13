import flet as ft
from flet_route import Params, Basket


def registerPageView(page: ft.Page, params: Params, basket: Basket):

    def snackBar(msg, color, time):
        page.snack_bar = ft.SnackBar(
                ft.Text(msg, size=17, weight=ft.FontWeight.BOLD),
                bgcolor=color,
                duration=time,
                )
        page.snack_bar.open = True
        page.update()
        
    def temp_page(e):
        page.go("/temp")
        
    return ft.View(
                    "/settings",
                    [
                        ft.AppBar(title=ft.Text("Settings"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.Text("Settings!", style="bodyMedium"),
                        ft.ElevatedButton(
                            "Go to Temp"
                            , on_click=temp_page
                        ),
                    ],
                )