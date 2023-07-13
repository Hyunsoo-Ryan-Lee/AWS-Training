import flet as ft
import shutil
def main(page:ft.Page):

    youlocation_file = ft.Text("")

    # CREATE FUNCTION OPEN FILE
    def dialog_picker(e:ft.FilePickerResultEvent):
        for x in e.files:
            print(x)
            # shutil.copy(x.name,f"myUploads/{x.name}")
            # # SET LOCATION FOLDER IMAGE
            # youlocation_file.value = f"myUploads/{x.name}"
            # youlocation_file.update()

    Mypick = ft.FilePicker(on_result=dialog_picker)
    page.overlay.append(Mypick)



    page.add(
        ft.Column([
            ft.ElevatedButton("Insert file",
                            on_click=lambda _: Mypick.pick_files(allow_multiple=True)
                            ),
            youlocation_file
                ])
         )

ft.app(target=main
       , name = ''
       , view = None
       , port = 2220
       )