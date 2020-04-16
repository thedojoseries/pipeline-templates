""" 
This Blueprint generates a CloudFormation template that deploys a VPC with a variable number of subnets whose addresses are calculated based on input parameters.  
"""

from troposphere import ec2
from troposphere import (
    Ref, Output, Join, FindInMap, Select, GetAZs, Tags,
    GetAtt, NoValue, Region, Sub
)

from stacker.blueprints.base import Blueprint
from stacker.blueprints.variables.types import TroposphereType

# These two packages should help you with the subnet address calculation
import math
import ipaddress

# This is the name of the resource in the final CloudFormation template. E.g.
# Resources:
#   VPC: <- HERE
#     Type:
#     Properties:
#       ...
VPC_NAME = "VPC"

# Ref returns an information about the resource provided. In the case of a VPC, Ref returns
# its ID. This is the same as doing in a CloudFormation template: !Ref VPC
VPC_ID = Ref(VPC_NAME)

# Since you will be deploying the VPC in us-east-1 (N. Virginia), here is the list of 
# available AZs
AZS = ["us-east-1a", "us-east-1b", "us-east-1c", "us-east-1d", "us-east-1e", "us-east-1f"]

class VPC(Blueprint):
    # These variables are the ones that you will have to specify in stacker-config.yaml when you call
    # this class
    VARIABLES = {
        "Namespace": {
            "type": str,
            "description": "The name of your team (team1, team2, team3)."
        },
        "VpcCidrBlock": {
            "type": str,
            "description": "The CIDR Block for the VPC."
        },
        "HostsPerSubnet": {
            "type": int,
            "description": "The maximum number of hosts for each subnet."
        }
    }

    def create_vpc(self):
        t = self.template
        t.add_resource(
          ec2.VPC(
            VPC_NAME,
            CidrBlock=self.get_variables()["VpcCidrBlock"], 
            EnableDnsSupport=True,
            EnableDnsHostnames=True,
            Tags=Tags(Name=self.get_variables()["Namespace"])
          )
        )

        t.add_output(Output("VpcId", Value=VPC_ID))

    def create_subnets(self):
        t = self.template

        vpc_cidr = self.get_variables()["VpcCidrBlock"]
        n_hosts = self.get_variables()["HostsPerSubnet"]
        
        # Calculate the number of subnets and their addresses here

        # For each calculated subnet
          t.add_resource(
              ec2.Subnet(
                  RESOURCE_NAME,
                  AvailabilityZone=AZS[?], # How can you distribute the subnets across as many AZs as possible?
                  VpcId=VPC_ID,
                  CidrBlock=SUBNET_CIDR_BLOCK, # This will come from the calculation above
                  Tags=Tags(Name="%s - %s" % (self.get_variables()["Namespace"], SUBNET_CIDR_BLOCK)) # This will generate the following tag: Name: teamX - x.x.x.x/x
              )
          )

    # This is a function that returns the final CloudFormation template to stacker. There is no need to explicitly "return" anything.
    def create_template(self):
        self.create_vpc()
        self.create_subnets()
