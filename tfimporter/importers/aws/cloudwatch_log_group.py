from typing import Dict, Any, Optional

from tfimporter import ObjectNotFoundException
from tfimporter.importers.aws import AwsImporter


class AwsCloudwatchLogGroupImporter(AwsImporter):

    def __init__(self):
        super().__init__()
        self.description = 'AWS Cloudwatch LOG group'

    def supports_resource(self, resource_provider: str, resource_type: str) -> bool:
        return resource_provider == "registry.terraform.io/hashicorp/aws" and resource_type == "aws_cloudwatch_log_group"

    def get_resource_id(self, element: Dict[str, Any], full_context: Dict[str, Any]) -> Optional[str]:

        provider_config_key = element.get("provider_config_key", "aws")
        name_prefix = element.get("values", {}).get("name_prefix")
        if name_prefix:
            raise Exception("Not available for new resources with prefix")

        log_group_arn = element.get("values", {}).get("arn")
        log_group_name = element.get("values", {}).get("name")
        if log_group_arn:
            return log_group_arn

        log_groups = []
        for page in self.get_aws_client('logs', full_context, provider_config_key).get_paginator('describe_log_groups').paginate(
                logGroupNamePrefix=log_group_name):
            for log_group_data in page.get("logGroups", []):
                if log_group_data["logGroupName"] == log_group_name:
                    log_groups.append(log_group_data)

        if not log_groups:
            raise ObjectNotFoundException()
        elif len(log_groups) > 1:
            raise Exception("Multiple log groups found")
        else:
            return log_groups[0]["logGroupName"]
