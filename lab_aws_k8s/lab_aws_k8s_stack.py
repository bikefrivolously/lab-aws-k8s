from aws_cdk import Stack, Tags
from constructs import Construct
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_iam as iam

import cdk_fck_nat


class LabAwsK8SStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        nat_provider = cdk_fck_nat.FckNatInstanceProvider(
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.T4G, ec2.InstanceSize.NANO
            )
        )
        vpc = ec2.Vpc(self, "k8-vpc", nat_gateway_provider=nat_provider, nat_gateways=1)
        nat_provider.security_group.add_ingress_rule(
            ec2.Peer.ipv4(vpc.vpc_cidr_block), ec2.Port.all_traffic()
        )

        with open("cp-userdata.txt", "r") as f:
            userdata = f.read()
        userdata_cp1 = ec2.UserData.for_linux(shebang="#!/bin/bash -xe")
        userdata_cp1.add_commands(userdata)
        instance_cp1 = ec2.Instance(
            self,
            "cp1",
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.T4G, ec2.InstanceSize.SMALL
            ),
            machine_image=ec2.MachineImage.latest_amazon_linux2023(
                cpu_type=ec2.AmazonLinuxCpuType.ARM_64, cached_in_context=True
            ),
            vpc=vpc,
            ssm_session_permissions=True,
            user_data_causes_replacement=True,
            user_data=userdata_cp1,
        )
        instance_cp1.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEKS_CNI_Policy")
        )

        Tags.of(instance_cp1).add(key="ssm", value="cp1")
