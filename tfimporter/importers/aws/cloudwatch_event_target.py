from pprint import pprint
from typing import Dict, Any, Optional

from tfimporter import MissingDependantObjectException, ObjectNotFoundException
from tfimporter.importers.aws import AwsImporter


class AwsCloudwatchEventTargetImporter(AwsImporter):

    def __init__(self):
        super().__init__()
        self.description = 'AWS Cloudwatch event target'

    def supports_resource(self, resource_provider: str, resource_type: str) -> bool:
        return resource_provider == "aws" and resource_type == "aws_cloudwatch_event_target"

    def get_resource_id(self, resource_provider: str, resource_type: str, terraform_resource_name: str, terraform_values: Dict[str, Any], full_context: Dict[str, Any]) -> Optional[str]:

        rule_name = terraform_values.get("rule")
        if not rule_name:
            raise MissingDependantObjectException("Parent rule not created yet")

        target_id = terraform_values.get("target_id")
        targets = []
        for page in self.get_aws_client('events', full_context).get_paginator("list_targets_by_rule").paginate(Rule=rule_name):
            for targets_data in page.get("Targets"):
                if targets_data["Id"] == target_id:
                    targets.append(targets_data)

        if not targets:
            raise ObjectNotFoundException()
        elif len(targets) > 1:
            raise Exception("Multiple targets found")
        else:
            return rule_name + "/" + targets[0]["Id"]
