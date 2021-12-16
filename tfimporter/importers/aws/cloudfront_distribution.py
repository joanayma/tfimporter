from pprint import pprint
from typing import Dict, Any, Optional

from tfimporter.importers.aws import AwsImporter
from tfimporter import ObjectNotFoundException


class AwsCloudfrontDistributionImporter(AwsImporter):

    def __init__(self):
        super().__init__()
        self.description = 'AWS Cloudfront Distribution'

    def supports_resource(self, resource_provider: str, resource_type: str) -> bool:
        return resource_provider == "registry.terraform.io/hashicorp/aws" and resource_type == "aws_cloudfront_distribution"

    def get_resource_id(self, element: Dict[str, Any], full_context: Dict[str, Any]) -> Optional[str]:
        provider_config_key = element.get("provider_config_key", "aws")
        comment = element.get("values", {}).get("comment")
        distributions = self.get_aws_client('cloudfront', full_context, provider_config_key).list_distributions()
        for distribution in distributions["DistributionList"]["Items"]:
            if distribution["Comment"] == comment:
                return distribution["Id"]
        raise ObjectNotFoundException()
