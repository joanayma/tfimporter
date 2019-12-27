from pprint import pprint
from typing import Dict, Any, Optional

from tfimporter.importers.aws import AwsImporter


class AwsCloudwatchEventRuleImporter(AwsImporter):

    def __init__(self):
        super().__init__()
        self.description = 'AWS Cloudwatch event rule'

    def supports_resource(self, resource_provider: str, resource_type: str) -> bool:
        return resource_provider == "aws" and resource_type == "aws_cloudwatch_event_rule"

    def get_resource_id(self, resource_provider: str, resource_type: str, terraform_resource_name: str, terraform_values: Dict[str, Any], full_context: Dict[str, Any]) -> Optional[str]:

        name_prefix = terraform_values.get("name_prefix")
        if name_prefix:
            raise Exception("Not available for new resources with prefix")

        rule_name = terraform_values.get("name")
        rules = []
        for page in self.get_aws_client('events', full_context).get_paginator("list_rules").paginate(NamePrefix=rule_name):
            for rules_data in page.get("Rules"):
                if rules_data["Name"] == rule_name:
                    rules.append(rules_data)

        if not rules:
            raise Exception("No rule found")
        elif len(rules) > 1:
            raise Exception("Multiple rules found")
        else:
            return rules[0]["Name"]
