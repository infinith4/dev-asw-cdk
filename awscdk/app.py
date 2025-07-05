#!/usr/bin/env python3
import os

import aws_cdk as cdk

from apprunner_stack import AppRunnerServiceStack # パスを調整してください

app = cdk.App()
AppRunnerServiceStack(app, "AppRunnerServiceStack",
    # 特定のリージョン/アカウントにデプロイする場合:
    # env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
)
app.synth()