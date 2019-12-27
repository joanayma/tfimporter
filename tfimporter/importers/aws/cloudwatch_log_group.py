from typing import Dict, Any, Optional

from tfimporter import ObjectNotFoundException
from tfimporter.importers.aws import AwsImporter


class AwsCloudwatchLogGroupImporter(AwsImporter):

    def __init__(self):
        super().__init__()
        self.description = 'AWS Cloudwatch LOG group'

    def supports_resource(self, resource_provider: str, resource_type: str) -> bool:
        return resource_provider == "aws" and resource_type == "aws_cloudwatch_log_group"

    def get_resource_id(self, resource_provider: str, resource_type: str, terraform_resource_name: str, terraform_values: Dict[str, Any], full_context: Dict[str, Any]) -> Optional[str]:

        name_prefix = terraform_values.get("name_prefix")
        if name_prefix:
            raise Exception("Not available for new resources with prefix")

        log_group_arn = terraform_values.get("arn")
        log_group_name = terraform_values.get("name")
        if log_group_arn:
            return log_group_arn

        log_groups = []
        for page in self.get_aws_client('logs', full_context).get_paginator('describe_log_groups').paginate(
                logGroupNamePrefix=log_group_name):
            for log_group_data in page.get("logGroups", []):
                if log_group_data["logGroupName"] == log_group_name:
                    log_groups.append(log_group_data)

        if not log_groups:
            raise ObjectNotFoundException()
        elif len(log_groups) > 1:
            raise Exception("Multiple LOG groups found")
        else:
            return log_groups[0]["logGroupName"]
