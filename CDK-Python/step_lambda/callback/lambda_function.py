import json
import boto3
import time

step = boto3.client('stepfunctions')

def lambda_handler(event, context):

    main_message=json.loads(event['Records'][0]['body'])
    print("Main Message Part : {}".format(main_message))
    
    step_function_input=main_message['input']

    task_token=main_message['MyTaskToken']
    print("The task token is : {}".format(task_token))
    
    time.sleep(7)
    
    response = step.send_task_success(
    taskToken=task_token,
    output=json.dumps({'body':'Return from Lambda Callback'})
    )