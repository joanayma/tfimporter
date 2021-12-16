from pprint import pprint
from typing import Dict, Any, Optional

from tfimporter.importers.aws import AwsImporter
from tfimporter import MissingDependantObjectException


class AwsS3BucketPolicyImporter(AwsImporter):

    def __init__(self):
        super().__init__()
        self.description = 'AWS S3 Bucket Policy'

    def supports_resource(self, resource_provider: str, resource_type: str) -> bool:
        return resource_provider == "registry.terraform.io/hashicorp/aws" and resource_type == "aws_s3_bucket_policy"

    def get_resource_id(self, element: Dict[str, Any], full_context: Dict[str, Any]) -> Optional[str]:
        provider_config_key = element.get("provider_config_key", "aws")
        bucket = element.get("values", {}).get("bucket")
        if not bucket:
            raise MissingDependantObjectException("the bucket value can't be calculated.")
        return bucket
