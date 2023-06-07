from aws_cdk import (
    aws_stepfunctions as _aws_stepfunctions,
    aws_stepfunctions_tasks as _aws_stepfunctions_tasks,
    aws_lambda as _lambda,
    aws_iam as iam,
    Duration,
    Stack,
)
from constructs import Construct


class StepFunctionLambda(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Lambda Handlers Definitions

        submit_lambda = _lambda.Function(
            self,
            "submitLambda",
            handler="lambda_function.lambda_handler",
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.from_asset("./step_lambda/submit"),
        )

        status_lambda = _lambda.Function(
            self,
            "statusLambda",
            handler="lambda_function.lambda_handler",
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.from_asset("./step_lambda/status"),
        )

        # Step functions Definition

        submit_job = _aws_stepfunctions_tasks.LambdaInvoke(
            self,
            "Submit Job",
            lambda_function=submit_lambda,
            output_path="$.Payload",
        )

        wait_job = _aws_stepfunctions.Wait(
            self,
            "Wait 10 Seconds",
            time=_aws_stepfunctions.WaitTime.duration(Duration.seconds(10)),
        )

        status_job = _aws_stepfunctions_tasks.LambdaInvoke(
            self,
            "Get Status",
            lambda_function=status_lambda,
            output_path="$.Payload",
        )

        fail_job = _aws_stepfunctions.Fail(
            self,
            "Fail",
            cause="AWS Batch Job Failed",
            error="DescribeJob returned FAILED",
        )

        succeed_job = _aws_stepfunctions.Succeed(
            self, "Succeeded", comment="AWS Batch Job succeeded"
        )

        # Create Chain

        definition = (
            submit_job.next(wait_job)
            .next(status_job)
            .next(
                _aws_stepfunctions.Choice(self, "Job Complete?")
                .when(
                    _aws_stepfunctions.Condition.string_equals("$.status", "FAILED"),
                    fail_job,
                )
                .when(
                    _aws_stepfunctions.Condition.string_equals("$.status", "SUCCEEDED"),
                    succeed_job,
                )
                .otherwise(wait_job)
            )
        )

        # role = iam.Role(
        #     self,
        #     "Role",
        #     role_name="StepFunctionCustomRole",
        #     assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
        # )
        # role.add_managed_policy(
        #     iam.ManagedPolicy.from_aws_managed_policy_name("AWSStepFunctionsFullAccess")
        # )
        # role.add_managed_policy(
        #     iam.ManagedPolicy.from_aws_managed_policy_name("AWSLambda_FullAccess")
        # )

        # Create state machine
        sm = _aws_stepfunctions.StateMachine(
            self,
            "StateMachine",
            state_machine_name="Sample-StateMachine",
            definition=definition,
            timeout=Duration.minutes(5),
        )
