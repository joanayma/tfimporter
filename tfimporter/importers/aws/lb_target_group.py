from pprint import pprint
from typing import Dict, Any, Optional

from tfimporter.importers.aws import AwsImporter


class AwsLbTargetGroupsImporter(AwsImporter):

    def __init__(self):
        super().__init__()
        self.description = 'AWS LoadBalancer Target Group'

    def supports_resource(self, resource_provider: str, resource_type: str) -> bool:
        return resource_provider == "registry.terraform.io/hashicorp/aws" and (
            resource_type == "aws_lb_target_group" or resource_type == "aws_alb_target_group")

    def get_resource_id(self, element: Dict[str, Any], full_context: Dict[str, Any]) -> Optional[str]:
        provider_config_key = element.get("provider_config_key", "aws")
        name = element.get("values", {}).get("name")
        result = self.get_aws_client('elbv2', full_context, provider_config_key).describe_target_groups(Names=[name])
        if len(result["TargetGroups"]) > 1:
            raise Exception(f"more than one result for LB {name}")
        return result["TargetGroups"][0]["TargetGroupArn"]
