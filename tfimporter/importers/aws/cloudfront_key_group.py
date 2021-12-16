from pprint import pprint
from typing import Dict, Any, Optional

from tfimporter.importers.aws import AwsImporter
from tfimporter import ObjectNotFoundException


class AwsCloudfrontKeyGroupImporter(AwsImporter):

    def __init__(self):
        super().__init__()
        self.description = 'AWS Cloudfront key group'

    def supports_resource(self, resource_provider: str, resource_type: str) -> bool:
        return resource_provider == "registry.terraform.io/hashicorp/aws" and resource_type == "aws_cloudfront_key_group"

    def get_resource_id(self, element: Dict[str, Any], full_context: Dict[str, Any]) -> Optional[str]:
        provider_config_key = element.get("provider_config_key", "aws")
        name = element.get("values", {}).get("name")
        key_groups = self.get_aws_client('cloudfront', full_context, provider_config_key).list_key_groups()
        for key_group in key_groups["KeyGroupList"]["Items"]:
            if key_group["KeyGroup"]["KeyGroupConfig"]["Name"] == name:
                return key_group["KeyGroup"]["Id"]
        raise ObjectNotFoundException(f"key group with name {name} not found")
