from aws_cdk import aws_iam as iam, Stack
from aws_cdk import aws_lambda as _lambda
from constructs import Construct


class MyConstruct(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        role = iam.Role.from_role_arn(
                self,
                'myRole',
                'arn:aws:iam::646664498184:role/EC2_SSM_Role'
            )

        _lambda.DockerImageFunction(
            self,
            'EcrLambda',
            code=_lambda.DockerImageCode.from_image_asset(directory='/home/ubuntu/AWS-Training/CDK-Python/cdk_python/lambda-image'),
            role=role,
            memory_size=128,
            architecture=_lambda.Architecture.ARM_64,
        )
        
        
        