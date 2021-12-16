from pprint import pprint
from typing import Dict, Any, Optional

from tfimporter.importers.aws import AwsImporter
from tfimporter import ObjectNotFoundException


class AwsCloudfrontOriginAccessIdentityImporter(AwsImporter):

    def __init__(self):
        super().__init__()
        self.description = 'AWS Cloudfront Origin Identity'

    def supports_resource(self, resource_provider: str, resource_type: str) -> bool:
        return resource_provider == "registry.terraform.io/hashicorp/aws" and resource_type == "aws_cloudfront_origin_access_identity"

    def get_resource_id(self, element: Dict[str, Any], full_context: Dict[str, Any]) -> Optional[str]:
        provider_config_key = element.get("provider_config_key", "aws")
        comment = element.get("values", {}).get("comment")
        origins = self.get_aws_client('cloudfront', full_context, provider_config_key).list_cloud_front_origin_access_identities()
        for origin in origins["CloudFrontOriginAccessIdentityList"]["Items"]:
            if origin["Comment"] == comment:
                return origin["Id"]
        raise ObjectNotFoundException()
