#!/usr/bin/env python3
from aws_cdk import App, Environment
from cdk_python.cdk_python_stack import CdkPythonStack
from cdk_python.python_ec2_stack import PythonEC2
from cdk_python.step_function_stack import StepFunctionLambda


app = App()
env_cn = Environment(account="646664498184", region="ap-northeast-2")

StepFunctionLambda(app, "StepFunction", env=env_cn)
# PythonEC2(app, "EC2Create", env=env_cn)
# PythonCdkStack(app, "PythonCdkStack")

app.synth()
