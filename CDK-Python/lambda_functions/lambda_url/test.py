import boto3

def list_ec2():
    # Create a Boto3 EC2 client
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
list_ec2()