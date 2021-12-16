from pprint import pprint
from typing import Dict, Any, Optional

from tfimporter import ObjectNotFoundException
from tfimporter.importers.aws import AwsImporter


class AwsCloudwatchMetricAlarmImporter(AwsImporter):

    def __init__(self):
        super().__init__()
        self.description = 'AWS Cloudwatch metric alarm'

    def supports_resource(self, resource_provider: str, resource_type: str) -> bool:
        return resource_provider == "registry.terraform.io/hashicorp/aws" and resource_type == "aws_cloudwatch_metric_alarm"

    def get_resource_id(self, element: Dict[str, Any], full_context: Dict[str, Any]) -> Optional[str]:
        return element.get("values", {}).get("alarm_name")
