from aws_cdk import (
    aws_lambda as _lambda,
    aws_iam as iam,
    Duration,
    Stack,
)

from constructs import Construct

class LambdaURLStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        role_arn = 'arn:aws:iam::646664498184:role/LambdaEC2FullAccessRole'
        role = iam.Role.from_role_arn(
                                    self, 
                                    "Role", 
                                    role_arn, 
                                    # mutable=False
                                    )
        
        private_lambda = _lambda.Function(
            self,
            "submitLambda",
            function_name = "CDK-URL-test",
            handler="lambda_function.lambda_handler",
            role=role,
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset("./lambda_functions/lambda_url"),
            timeout = Duration.seconds(60)
        )
        
        private_lambda.add_function_url(auth_type=_lambda.FunctionUrlAuthType.NONE)