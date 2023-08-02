import os
import flet as ft
from flet_route import Routing, path
from uploader_main import mainPageView
from uploader_auth import authPageView
from dotenv import load_dotenv

load_dotenv()

def main(page: ft.Page):
    page.title = ""
    page.bgcolor = ft.colors.BLACK45
    page.scroll = "always"
    
    app_routes = [
        path(url='/', clear=True, view=authPageView),
        path(url='/cksdbwlsdb', clear=True, view=mainPageView)
    ]
    
    Routing(page=page, app_routes=app_routes)
    
    page.go(page.route)
    page.update()


ft.app(target=main
    , upload_dir=os.environ.get('UPLOAD_DIR_NAME')
    , port = 2000
    , view=ft.WEB_BROWSER)
    