#!/usr/bin/env python3
import os

import aws_cdk as cdk

from lab_aws_k8s.lab_aws_k8s_stack import LabAwsK8SStack


app = cdk.App()
LabAwsK8SStack(
    app,
    "LabAwsK8SStack",
    env=cdk.Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

app.synth()
