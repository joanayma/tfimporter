from pprint import pprint
from typing import Dict, Any, Optional

from tfimporter import MissingDependantObjectException
from tfimporter.importers.aws import AwsImporter


class AwsSecurityGroupImporter(AwsImporter):

    def __init__(self):
        super().__init__()
        self.description = 'AWS security group'

    def supports_resource(self, resource_provider: str, resource_type: str) -> bool:
        return resource_provider == "aws" and resource_type == "aws_security_group"

    def get_resource_id(self, resource_provider: str, resource_type: str, terraform_resource_name: str, terraform_values: Dict[str, Any], full_context: Dict[str, Any]) -> Optional[str]:

        name_prefix = terraform_values.get("name_prefix")
        if name_prefix:
            raise Exception("Not available for new resources with prefix")

        vpc_id = terraform_values.get("vpc_id")
        if not vpc_id:
            raise MissingDependantObjectException("Parent VPC not created yet")

        security_group_name = terraform_values.get("name")
        for page in self.get_aws_client('ec2', full_context).get_paginator("describe_security_groups").paginate(Filters=[{"Name": "vpc-id", "Values": [vpc_id]}, {"Name": "group-name", "Values": [security_group_name]}]):
            for security_group_data in page.get("SecurityGroups"):
                return security_group_data.get("GroupId")
        return None
