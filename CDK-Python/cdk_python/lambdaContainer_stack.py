import os
import typing
from aws_cdk import (
    aws_lambda,
    aws_ecr,
    aws_iam as iam,
    Aws, Duration, Stack
)
from constructs import Construct


class LambdaContainerFunctionStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        image_name    = "lambdaContainerFunction"
        use_pre_existing_image = False


        if (use_pre_existing_image):

            ecr_repository = aws_ecr.Repository.from_repository_attributes(self,
                id              = "ECR",
                repository_arn  ='arn:aws:ecr:{0}:{1}'.format(Aws.REGION, Aws.ACCOUNT_ID),
                repository_name = image_name
            ) ## aws_ecr.Repository.from_repository_attributes

            ecr_image = typing.cast("aws_lambda.Code", aws_lambda.EcrImageCode(
                repository = ecr_repository,
                tag='latest'
            )) ## aws_lambda.EcrImageCode

        else:
            ecr_image = aws_lambda.EcrImageCode.from_asset_image(
                directory = "/home/ubuntu/AWS-Training/CDK-Python/cdk_python/lambda-image",
            )
        
        # Lambda 함수의 IAM Role 정의   
        role_arn = 'arn:aws:iam::646664498184:role/LambdaEC2FullAccessRole'
        role = iam.Role.from_role_arn(
                                    self, 
                                    "Role", 
                                    role_arn, 
                                    # mutable=False
                                    )

        # 람다 함수 부분
        aws_lambda.Function(self,
          id            = "lambdaContainerFunction",
          description   = "Lambda Container Function",
          role          = role,
          code          = ecr_image,
          handler       = aws_lambda.Handler.FROM_IMAGE,
          runtime       = aws_lambda.Runtime.FROM_IMAGE,
          environment   = {"hello":"world"},
          function_name = "LambdaDockerImage",
          memory_size   = 128,
          reserved_concurrent_executions = 10,
          timeout       = Duration.seconds(30)
        )