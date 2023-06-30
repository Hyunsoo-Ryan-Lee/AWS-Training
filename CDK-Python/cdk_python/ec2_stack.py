from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    Stack,
)
from constructs import Construct
from aws_cdk.aws_s3_assets import Asset

# user_data_res["Fn::Join"] = ["", user_data.splitlines(True)]


class PythonEC2(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Ubuntu 20.04
        img = ec2.MachineImage.generic_linux(
            {"ap-northeast-2": "ami-04341a215040f91bb"}
        )
        
        ''' 새로운 Role 생성시 
        role = iam.Role(
            self,
            "IAM_Role",
            role_name="EC2_SSM_Role",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com")
        )
        role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("CloudFrontFullAccess")
        )
        role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonSSMManagedInstanceCore"
            )
        )
        '''
        role_arn = 'arn:aws:iam::646664498184:role/EC2_SSM_Role'
        role = iam.Role.from_role_arn(
                                    self, 
                                    "Role", 
                                    role_arn, 
                                    # mutable=False
                                    )
        role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("CloudFrontFullAccess")
        )

        vpc = ec2.Vpc(
            self,
            "devVPC",
            cidr="10.1.0.0/16",
            max_azs=2,
            enable_dns_hostnames=True,
            enable_dns_support=True,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Public-cdk", subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="Private-cdk",
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                    cidr_mask=24,
                ),
            ],
            nat_gateways=1,
        )
        security_group = ec2.SecurityGroup(
            self, "CDK-SecurityGroup", vpc=vpc, allow_all_outbound=True
        )

        # Inbound Rules
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "SSH access"
        )
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "HTTP access"
        )
        
        '''
        vpc = ec2.Vpc.from_lookup(self, "VPC")
        security_group_id = "sg-083c7967737299150"  # Replace with your security group ID
        security_group = ec2.SecurityGroup.from_lookup_by_id(self, "aws-stack-group", security_group_id)
        '''
        
        with open("/home/ubuntu/user-data.sh") as f:
            user_data = f.read()

        instance = ec2.Instance(
            self,
            "CDK-Instance",
            instance_name="mySingleHost",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=img,
            vpc=vpc,
            role = role,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            key_name="K8S",
            security_group=security_group,
            ssm_session_permissions=True,
            user_data=ec2.UserData.custom(user_data),
        )