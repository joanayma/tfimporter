from pprint import pprint
from typing import Dict, Any, Optional

from tfimporter.importers.aws import AwsImporter
from tfimporter import ObjectNotFoundException


class AwsCloudfrontPublicKeyImporter(AwsImporter):

    def __init__(self):
        super().__init__()
        self.description = 'AWS Cloudfront public key'

    def supports_resource(self, resource_provider: str, resource_type: str) -> bool:
        return resource_provider == "registry.terraform.io/hashicorp/aws" and resource_type == "aws_cloudfront_public_key"

    def get_resource_id(self, element: Dict[str, Any], full_context: Dict[str, Any]) -> Optional[str]:
        provider_config_key = element.get("provider_config_key", "aws")
        name = element.get("values", {}).get("name")
        distributions = self.get_aws_client('cloudfront', full_context, provider_config_key).list_public_keys()
        for distribution in distributions["PublicKeyList"]["Items"]:
            if distribution["Name"] == name:
                return distribution["Id"]
        raise ObjectNotFoundException()
