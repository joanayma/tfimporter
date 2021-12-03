from pprint import pprint
from typing import Dict, Any, Optional

from tfimporter import MissingDependantObjectException
from tfimporter.importers.aws import AwsImporter


class AwsIamRolePolicyImporter(AwsImporter):

    def __init__(self):
        super().__init__()
        self.description = 'AWS IAM role policy'

    def supports_resource(self, resource_provider: str, resource_type: str) -> bool:
        return resource_provider == "registry.terraform.io/hashicorp/aws" and resource_type == "aws_iam_role_policy"

    def get_resource_id(self, element: Dict[str, Any], full_context: Dict[str, Any]) -> Optional[str]:

        provider_config_key = element.get("provider_config_key", "aws")
        name_prefix = element.get("values", {}).get("name_prefix")
        if name_prefix:
            raise Exception("Not available for new resources with prefix")

        role_name = element.get("values", {}).get("role")
        if not role_name:
            raise MissingDependantObjectException("Parent role not created yet")

        policy_name = element.get("values", {}).get("name")
        response = self.get_aws_client('iam', full_context, provider_config_key).get_role_policy(RoleName=role_name, PolicyName=policy_name)
        return response.get("RoleName") + ":" + response.get("PolicyName")
