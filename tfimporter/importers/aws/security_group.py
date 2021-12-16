from pprint import pprint
from typing import Dict, Any, Optional

from tfimporter import MissingDependantObjectException
from tfimporter.importers.aws import AwsImporter


class AwsSecurityGroupImporter(AwsImporter):

    def __init__(self):
        super().__init__()
        self.description = 'AWS security group'

    def supports_resource(self, resource_provider: str, resource_type: str) -> bool:
        return resource_provider == "registry.terraform.io/hashicorp/aws" and resource_type == "aws_security_group"

    def get_resource_id(self, element: Dict[str, Any], full_context: Dict[str, Any]) -> Optional[str]:
        provider_config_key = element.get("provider_config_key", "aws")
        name_prefix = element.get("values", {}).get("name_prefix")
        if name_prefix:
            raise Exception("Not available for new resources with prefix")

        vpc_id = element.get("values", {}).get("vpc_id")
        if not vpc_id:
            raise MissingDependantObjectException("Parent VPC not created yet")

        security_group_name = element.get("values", {}).get("name")
        for page in self.get_aws_client('ec2', full_context, provider_config_key).get_paginator("describe_security_groups").paginate(Filters=[{"Name": "vpc-id", "Values": [vpc_id]}, {"Name": "group-name", "Values": [security_group_name]}]):
            for security_group_data in page.get("SecurityGroups"):
                return security_group_data.get("GroupId")
        return None
