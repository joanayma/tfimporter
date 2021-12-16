from pprint import pprint
from typing import Dict, Any, Optional

from tfimporter.importers.aws import AwsImporter
from tfimporter import MissingDependantObjectException


class AwsIamRolePolicyAttachmentImporter(AwsImporter):

    def __init__(self):
        super().__init__()
        self.description = 'AWS IAM role policy attachment'

    def supports_resource(self, resource_provider: str, resource_type: str) -> bool:
        return resource_provider == "registry.terraform.io/hashicorp/aws" and resource_type == "aws_iam_role_policy_attachment"

    def get_resource_id(self, element: Dict[str, Any], full_context: Dict[str, Any]) -> Optional[str]:
        provider_config_key = element.get("provider_config_key", "aws")
        role = element.get("values", {}).get("role")
        if not role:
            raise MissingDependantObjectException("the role can't be calculated.")
        policy_arn = element.get("values", {}).get("policy_arn")
        if not policy_arn:
            raise MissingDependantObjectException("the policy arn can't be calculated.")
        return role + "/" + policy_arn
