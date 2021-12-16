from pprint import pprint
from typing import Dict, Any, Optional

from tfimporter import MissingDependantObjectException
from tfimporter.importers.aws import AwsImporter


class AwsLbListenerRuleImporter(AwsImporter):

    def __init__(self):
        super().__init__()
        self.description = 'AWS LoadBalancer Listener Rule'

    def supports_resource(self, resource_provider: str, resource_type: str) -> bool:
        return resource_provider == "registry.terraform.io/hashicorp/aws" and (
            resource_type == "aws_lb_listener_rule" or resource_type == "aws_alb_listener_rule")

    def get_resource_id(self, element: Dict[str, Any], full_context: Dict[str, Any]) -> Optional[str]:
        provider_config_key = element.get("provider_config_key", "aws")
        name_prefix = element.get("values", {}).get("name_prefix")
        if name_prefix:
            raise Exception("Not available for new resources with prefix")
        listener_arn = element.get("values", {}).get("listener_arn")
        if not listener_arn:
            raise MissingDependantObjectException(f"listener arn can't be calculated.")
        rules = self.get_aws_client('elbv2', full_context, provider_config_key).describe_rules(ListenerArn=listener_arn)
        for rule in rules["Rules"]:
            return rule["RuleArn"]
