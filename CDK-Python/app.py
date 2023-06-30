#!/usr/bin/env python3
from aws_cdk import App, Environment
from cdk_python.cdk_python_stack import CdkPythonStack
from cdk_python.ec2_stack import PythonEC2
from cdk_python.step_function_stack import StepFunctionLambda
from cdk_python.step_function_callback import StepFunctionCallBack
from cdk_python.lambda_stack import LambdaURLStack


app = App()
env_cn = Environment(account="646664498184", region="ap-northeast-2")

LambdaURLStack(app, "LambdaURL", env=env_cn)
# StepFunctionCallBack(app, "StepFunctionCall", env=env_cn)
# StepFunctionLambda(app, "StepFunction", env=env_cn)
# PythonEC2(app, "EC2Create", env=env_cn)
# PythonCdkStack(app, "PythonCdkStack")

app.synth()
