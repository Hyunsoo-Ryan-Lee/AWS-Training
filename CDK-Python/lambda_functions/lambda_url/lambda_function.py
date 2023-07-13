import json
import boto3
from collections import Counter
from script import html_title, html_buttons, html_scripts


def start_stop_ec2(instance_name, command):
    ec2_client = boto3.client('ec2')
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
    
    instances, instance_states = [], []
    dividor = "_____"
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            # instance_id = instance['InstanceId']
            instance_type = instance['InstanceType']
            state = instance['State']['Name']
            instance_states.append(state)
            
            name = ''
            for tag in instance['Tags']:
                if tag['Key'] == 'Name':
                    name = tag['Value']
            
            instances.append(f"{name}({instance_type}){dividor}{state}")
    instances.sort(key=lambda x : (x.split(dividor)[1], x.split(dividor)[0].lower()))

    return instances, instance_states


def lambda_handler(event, context):
    events = event["requestContext"]["http"]
    # print("Client IP : ",events["sourceIp"])
    ec2_names, instance_states = list_ec2()
    
    dropdown_options = []
    for name in ec2_names:
        dropdown_options.append(f"<option value='{name}'>{name}</option>")
    dropdown_menu = '\n' + '\n'.join(dropdown_options) + '\n'
    
    pre_options = ""
    counts = Counter(instance_states)
    most_common_elements = counts.most_common()
    for element, count in most_common_elements:
        scr = f"<pre>        {element} : {count} </pre>\n"
        pre_options += scr
    pre_options = "\n" + pre_options
    
    html = html_title \
            + dropdown_menu \
            + html_buttons \
            + pre_options \
            + html_scripts
    
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