from pprint import pprint
from typing import Dict, Any, Optional

from tfimporter.importers.aws import AwsImporter


class AwsS3BucketImporter(AwsImporter):

    def __init__(self):
        super().__init__()
        self.description = 'AWS S3 Bucket'

    def supports_resource(self, resource_provider: str, resource_type: str) -> bool:
        return resource_provider == "registry.terraform.io/hashicorp/aws" and resource_type == "aws_s3_bucket"

    def get_resource_id(self, element: Dict[str, Any], full_context: Dict[str, Any]) -> Optional[str]:
        return element.get("values", {}).get("bucket")
