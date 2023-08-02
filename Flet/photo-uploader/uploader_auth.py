import flet as ft
from flet_route import Params, Basket



def authPageView(page: ft.Page, params: Params, basket: Basket):
    page.bgcolor = ft.colors.BLACK45
    page.scroll = "always"
    def snackBar(msg, color, time):
        page.snack_bar = ft.SnackBar(
                ft.Text(msg, size=17, weight=ft.FontWeight.BOLD),
                bgcolor=color,
                duration=time,
                )
        page.snack_bar.open = True
        page.update()
        
    def to_main():
        page.go("/cksdbwlsdb")
        
    def validate_password(e, passwd):
        if passwd == "150808":
            to_main()
            snackBar("WELCOME!", 'GREEN', 3000)
        else:
            snackBar("ENTER VALID PASSWORD", 'RED', 3000)
            passwd_field.value = ""
            page.update()
        
    passwd_field = ft.TextField(
        label="password",
        keyboard_type='NUMBER',
        border="underline",
        width=320,
        height=100,
        text_size=25,
        color='BLUE',
        password=True,
        can_reveal_password=True
    )
    
    btn1 = ft.FilledButton(content=ft.Text("Login", weight="w700")
                           , width=140
                           , height=40
                           , icon_color= "green"
                           , on_click=lambda e: validate_password(e, passwd_field.value)
                           )
        
    return ft.View(
                    "/",
                    [ft.Column(controls=[passwd_field, btn1], alignment=ft.alignment.center)]
                )