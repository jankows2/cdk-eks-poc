import aws_cdk as core
import aws_cdk.assertions as assertions
from cdk_eks_poc.cdk_eks_poc_stack import CdkEksPocStack


def test_sqs_queue_created():
    app = core.App()
    stack = CdkEksPocStack(app, "cdk-eks-poc")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::SQS::Queue", {
        "VisibilityTimeout": 300
    })


def test_sns_topic_created():
    app = core.App()
    stack = CdkEksPocStack(app, "cdk-eks-poc")
    template = assertions.Template.from_stack(stack)

    template.resource_count_is("AWS::SNS::Topic", 1)
