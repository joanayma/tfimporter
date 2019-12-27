from pprint import pprint
from typing import Dict, Any, Optional

from tfimporter import MissingDependantObjectException
from tfimporter.importers.aws import AwsImporter


class AwsSecurityGroupRuleImporter(AwsImporter):

    def __init__(self):
        super().__init__()
        self.description = 'AWS security group rule'

    def supports_resource(self, resource_provider: str, resource_type: str) -> bool:
        return resource_provider == "aws" and resource_type == "aws_security_group_rule"

    def get_resource_id(self, resource_provider: str, resource_type: str, terraform_resource_name: str, terraform_values: Dict[str, Any], full_context: Dict[str, Any]) -> Optional[str]:
        security_group_id = terraform_values.get("security_group_id")
        if not security_group_id:
            raise MissingDependantObjectException("Parent security group not created yet")
        raise Exception("Security group rules should have been imported automatically when importing parent security groups")
