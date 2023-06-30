import json
import boto3
from html_script import html_1, html_2

def start_stop_ec2(instance_name, command):
    ec2 = boto3.resource('ec2')
    instances = ec2.instances.filter(Filters=[{'Name': 'tag:Name', 'Values': [instance_name]}])
    for instance in instances:
        if command == 'start': instance.start()
        if command == 'stop' : instance.stop()
        msg = f"Starting EC2 instance with name: {instance_name} (Instance ID: {instance.id})"
        break
    else:
        msg = f"No EC2 instances found with name: {instance_name}"
        print(msg)


def list_ec2():
    ec2_client = boto3.client('ec2')
    
    response = ec2_client.describe_instances()
    
    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            # instance_id = instance['InstanceId']
            instance_type = instance['InstanceType']
            state = instance['State']['Name']
            
            name = ''
            for tag in instance['Tags']:
                if tag['Key'] == 'Name':
                    name = tag['Value']
            
            instances.append(f"{name}({instance_type})____{state}")
    return instances   

def lambda_handler(event, context):
    events = event["requestContext"]["http"]
    
    ec2_names = list_ec2()
    dropdown_options = []
    for i, name in enumerate(ec2_names):
        dropdown_options.append(f"<option value='instance_{i}'>{name}</option>")
    dropdown_menu = '\n' + '\n'.join(dropdown_options) + '\n'
    
    html = html_1 + dropdown_menu + html_2
    
    if events["method"] == "GET":
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "text/html",
            },
            "body": html
        }
    elif events["method"] == "POST":
        if events["path"] == "/start-ec2":
            data = json.loads(event["body"])
            name = data.get("instance_name", "")
            start_stop_ec2(name, 'start')
            
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "text/plain",
                },
                "body": "EC2 instance start request received"
            }
        elif events["path"] == "/stop-ec2":
            data = json.loads(event["body"])
            name = data.get("instance_name", "")
            start_stop_ec2(name, 'stop')
            
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "text/plain",
                },
                "body": "EC2 instance start request received"
            }
        else:
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "text/plain",
                },
                "body": f"Hello, {name}!"
            }
