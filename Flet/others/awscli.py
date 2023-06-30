import flet as ft
import boto3
import subprocess




def main(page: ft.Page):
    page.title = "Basic text buttons"
    page.bgcolor = 'WHITE'
    def cli_command(e):
        command = "aws s3 ls"
        output = subprocess.check_output(command, shell=True).decode().strip()
        print(output)

    def start_ec2_instance(instance_id):
        ec2_client = boto3.client('ec2')
        ec2 = boto3.resource('ec2')
        instance_name = inst_name.value
        instances = ec2.instances.filter(Filters=[{'Name': 'tag:Name', 'Values': [instance_name]}])
        for instance in instances:
            instance.stop()
            msg = f"Starting EC2 instance with name: {instance_name} (Instance ID: {instance.id})"
            break
        else:
            msg = f"No EC2 instances found with name: {instance_name}"
            cnt1.value = msg
            page.snack_bar = ft.SnackBar(ft.Text("EC2 instances found"), duration=1000)
            page.snack_bar.open = True
            page.update()
            
    def erase(e):
        cnt1.value = ""
        page.update()

    
    
    inst_name = ft.TextField(label="EC2 ID")
    btn1 = ft.TextButton(text="AWS CLI", on_click=start_ec2_instance)
    btn2 = ft.OutlinedButton(text="EMPTY", on_click=erase)
    img = ft.Image(
        src=f"https://personal-golight-image-bucket.s3.ap-northeast-2.amazonaws.com/sample/000174400032_29.jpg",
        width=100,
        height=100,
        fit=ft.ImageFit.CONTAIN,
    )
    cnt1 = ft.TextField(width=1000, height=500, multiline=True)

    
    page.add(
        inst_name,
        btn1,
        cnt1,
        btn2
    )


ft.app(port = 3456
       , target=main
       , view=ft.WEB_BROWSER
       )