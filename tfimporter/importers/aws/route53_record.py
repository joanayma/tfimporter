from pprint import pprint
from typing import Dict, Any, Optional

from tfimporter.importers.aws import AwsImporter


class AwsRoute53RecordImporter(AwsImporter):

    def __init__(self):
        super().__init__()
        self.description = 'AWS Route53 Record'

    def supports_resource(self, resource_provider: str, resource_type: str) -> bool:
        return resource_provider == "registry.terraform.io/hashicorp/aws" and resource_type == "aws_route53_record"

    def get_resource_id(self, element: Dict[str, Any], full_context: Dict[str, Any]) -> Optional[str]:
        name = element.get("values").get("name")
        zone_id = element.get("values").get("zone_id")
        record_type = element.get("values").get("type")
        return zone_id + "_" + name + "_" + record_type
