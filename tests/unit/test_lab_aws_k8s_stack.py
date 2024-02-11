import aws_cdk as core
import aws_cdk.assertions as assertions

from lab_aws_k8s.lab_aws_k8s_stack import LabAwsK8SStack

# example tests. To run these tests, uncomment this file along with the example
# resource in lab_aws_k8s/lab_aws_k8s_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = LabAwsK8SStack(app, "lab-aws-k8s")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
