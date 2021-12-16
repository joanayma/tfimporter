from pprint import pprint
from typing import Dict, Any, Optional

from tfimporter import MissingDependantObjectException, ObjectNotFoundException
from tfimporter.importers.aws import AwsImporter


class AwsCloudwatchEventTargetImporter(AwsImporter):

    def __init__(self):
        super().__init__()
        self.description = 'AWS Cloudwatch event target'

    def supports_resource(self, resource_provider: str, resource_type: str) -> bool:
        return resource_provider == "registry.terraform.io/hashicorp/aws" and resource_type == "aws_cloudwatch_event_target"

    def get_resource_id(self, element: Dict[str, Any], full_context: Dict[str, Any]) -> Optional[str]:
        provider_config_key = element.get("provider_config_key", "aws")
        rule_name = element.get("values", {}).get("rule")
        if not rule_name:
            raise MissingDependantObjectException("Parent rule not created yet")
        arn = element.get("values", {}).get("arn")
        for page in self.get_aws_client('events', full_context, provider_config_key).get_paginator("list_targets_by_rule").paginate(Rule=rule_name):
            for target in page.get("Targets"):
                if target["Arn"] == arn:
                    return rule_name + "/" + target["Id"]
