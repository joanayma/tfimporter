from pprint import pprint
from typing import Dict, Any, Optional

from tfimporter import MissingDependantObjectException, NoOpException
from tfimporter.importers.aws import AwsImporter


class AwsSecurityGroupRuleImporter(AwsImporter):

    def __init__(self):
        super().__init__()
        self.description = 'AWS security group rule'

    def supports_resource(self, resource_provider: str, resource_type: str) -> bool:
        return resource_provider == "registry.terraform.io/hashicorp/aws" and resource_type == "aws_security_group_rule"

    def get_resource_id(self, element: Dict[str, Any], full_context: Dict[str, Any]) -> Optional[str]:
        provider_config_key = element.get("provider_config_key", "aws")
        security_group_id = element.get("values", {}).get("security_group_id")
        if not security_group_id:
            raise MissingDependantObjectException("Parent security group not imported or created yet")
        raise NoOpException("Security group rules should have been imported automatically when importing parent security groups")
