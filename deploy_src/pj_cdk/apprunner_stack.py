from aws_cdk import (
    Stack,
    aws_apprunner as apprunner,
    aws_iam as iam,
    Duration,
)
from constructs import Construct

class AppRunnerServiceStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # --- 1. (Optional) Create an IAM role for the App Runner service
        # This role grants permissions to your application running inside App Runner
        # to interact with other AWS services (e.g., S3, DynamoDB, etc.).
        instance_role = iam.Role(
            self,
            "AppRunnerInstanceRole",
            assumed_by=iam.ServicePrincipal("tasks.apprunner.amazonaws.com"),
            description="IAM role for App Runner service instances to access AWS resources",
        )

        # Example: Granting read-only access to S3 (Uncomment if needed)
        # instance_role.add_to_policy(
        #     iam.PolicyStatement(
        #         actions=["s3:GetObject", "s3:ListBucket"],
        #         resources=["arn:aws:s3:::your-bucket-name", "arn:aws:s3:::your-bucket-name/*"],
        #     )
        # )

        # --- 2. Create the AWS App Runner Service
        apprunner.CfnService(
            self,
            "MyWebAppRunnerService",
            service_name="my-web-app-runner-service", # Choose a unique name for your service
            source_configuration=apprunner.CfnService.SourceConfigurationProperty(
                image_repository=apprunner.CfnService.ImageRepositoryProperty(
                    image_identifier="public.ecr.aws/aws-containers/hello-app-runner:latest", # REPLACE with your actual image URI
                    image_repository_type="ECR_PUBLIC", # Or "ECR" if your image is in private ECR

                    # If you use a private ECR repository, you'll need a connection ARN:
                    # image_configuration=apprunner.CfnService.ImageConfigurationProperty(
                    #   # port="8080", # Default port for hello-app-runner example
                    #   runtime_environment_variables=[
                    #       apprunner.CfnService.KeyValuePairProperty(name="PORT", value="8080")
                    #   ],
                    # ),
                ),
                # For private ECR, you might need a connection
                # authentication_configuration=apprunner.CfnService.AuthenticationConfigurationProperty(
                #   connection_arn="arn:aws:apprunner:REGION:ACCOUNT_ID:connection/YOUR_CONNECTION_NAME",
                # ),
            ),
            instance_configuration=apprunner.CfnService.InstanceConfigurationProperty(
                cpu="1024", # 1 vCPU
                memory="2048", # 2 GB
                instance_role_arn=instance_role.role_arn, # Attach the instance role
            ),
            # health_check_configuration=apprunner.CfnService.HealthCheckConfigurationProperty( # Optional: Custom health check
            #     protocol="HTTP",
            #     path="/health",
            #     interval=Duration.seconds(10).to_seconds(),
            #     timeout=Duration.seconds(5).to_seconds(),
            #     healthy_threshold=1,
            #     unhealthy_threshold=5,
            # ),
            network_configuration=apprunner.CfnService.NetworkConfigurationProperty(
                # Optional: VPC Connector to connect to resources in a VPC
                # egress_configuration=apprunner.CfnService.EgressConfigurationProperty(
                #     egress_type="VPC_CONNECTOR",
                #     vpc_connector_arn="arn:aws:apprunner:REGION:ACCOUNT_ID:vpcconnector/YOUR_VPC_CONNECTOR_NAME",
                # ),
            ),
            # Use default auto-scaling configuration
            # auto_scaling_configuration_arn=apprunner.AutoScalingConfiguration.from_auto_scaling_configuration_name(
            #     self,
            #     "DefaultAutoScalingConfig",
            #     "DefaultAutoScalingConfiguration"
            # ).auto_scaling_configuration_arn,
            # encryption_configuration=apprunner.CfnService.EncryptionConfigurationProperty( # Optional: Custom KMS key for encryption at rest
            #   kms_key="arn:aws:kms:REGION:ACCOUNT_ID:key/YOUR_KMS_KEY_ID",
            # ),
        )