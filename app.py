#!/usr/bin/env python3

# There is a good documentation of all supported resources, from node groups
# to alb controllers, and networking.
# https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_eks/README.html

from constructs import Construct
from aws_cdk import (
    aws_ec2 as ec2,
    aws_eks as eks,
    App, Stack
)

class EKSCluster(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, *kwargs)

        #vpc = ec2.Vpc("eks-poc-vpc", max_azs=3)
        vpc = ec2.Vpc(
            self, "eks-poc-vpc",
            max_azs=3
        )


        # provisiong a cluster
        # When no vpc is specified, one is created by default.
        # Might need to check out VPC creation to make sure it's following our policy
        cluster = eks.Cluster(self, "eks-poc",
            version=eks.KubernetesVersion.V1_21,
            vpc=vpc,
            endpoint_access=eks.EndpointAccess.PRIVATE,
            alb_controller=eks.AlbControllerOptions(
                version=eks.AlbControllerVersion.V2_3_1
            ),
            default_capacity=0
        )

        cluster.add_nodegroup_capacity("custom-node-group",
            instance_types=[ec2.InstanceType("m5.large")],
            min_size=4,
            disk_size=100,
            ami_type=eks.NodegroupAmiType.AL2_X86_64
        )

        # apply a kubernetes manifest to the cluster
        # we can specify our image here for testing
        cluster.add_manifest("mypod", {
            "api_version": "v1",
            "kind": "Pod",
            "metadata": {"name": "mypod"},
            "spec": {
                "containers": [{
                    "name": "hello",
                    "image": "paulbouwer/hello-kubernetes:1.5",
                    "ports": [{"container_port": 8080}]
                }
                ]
            }
        })

app = App()
EKSCluster(app, "EKS-POC-CLUSTER")
app.synth()
