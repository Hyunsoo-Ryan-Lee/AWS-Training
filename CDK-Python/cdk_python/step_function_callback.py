from aws_cdk import (
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as sfn_tasks,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_sqs as sqs,
    Duration,
    Stack,
)

from aws_cdk.aws_lambda_event_sources import SqsEventSource
from constructs import Construct

queue_arn = "arn:aws:sqs:ap-northeast-2:646664498184:CallBackQueue"

class StepFunctionCallBack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)


        queue = sqs.Queue.from_queue_arn(self, "MyQueue", queue_arn)
        
        callback_lambda = _lambda.Function(
            self,
            "submitLambda",
            function_name = "CDK-CallBack",
            handler="lambda_function.lambda_handler",
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.from_asset("./step_lambda/callback"),
            timeout = Duration.seconds(30)
        )
        # SQS Trigger 연결
        callback_lambda.add_event_source(SqsEventSource(queue))


        # Step functions Definition
        succeed_job = sfn.Succeed(
            self, "Succeeded", comment="AWS Batch Job succeeded"
        )
        
        sqs_job = sfn_tasks.SqsSendMessage(self, "SQSSendMessage",
                            queue=queue,
                            integration_pattern=sfn.IntegrationPattern.WAIT_FOR_TASK_TOKEN,
                            message_body=sfn.TaskInput.from_object({
                                        "MyTaskToken": sfn.JsonPath.task_token,
                                        "input": sfn.JsonPath.string_at("$")
                                    })
                            )

        # Create Chain
        definition = (
            sqs_job.next(succeed_job)
        )

        # Create IAM Role
        role = iam.Role(
            self,
            "Role",
            role_name="StepFunctionCustomRole",
            assumed_by=iam.ServicePrincipal("states.amazonaws.com"),
        )
        role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AWSStepFunctionsFullAccess")
        )
        role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AWSLambda_FullAccess")
        )
        role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSQSFullAccess")
        )

        # Create state machine
        sm = sfn.StateMachine(
            self,
            "StateMachine",
            state_machine_name="Second-StateMachine",
            role=role,
            definition=definition,
            timeout=Duration.minutes(5),
        )
