from pprint import pprint
from typing import Dict, Any, Optional

from tfimporter import MissingDependantObjectException
from tfimporter.importers.aws import AwsImporter


class AwsLbListenerImporter(AwsImporter):

    def __init__(self):
        super().__init__()
        self.description = 'AWS LoadBalancer Listener'

    def supports_resource(self, resource_provider: str, resource_type: str) -> bool:
        return resource_provider == "registry.terraform.io/hashicorp/aws" and (
            resource_type == "aws_lb_listener" or resource_type == "aws_alb_listener")

    def get_resource_id(self, element: Dict[str, Any], full_context: Dict[str, Any]) -> Optional[str]:
        provider_config_key = element.get("provider_config_key", "aws")
        name_prefix = element.get("values", {}).get("name_prefix")
        if name_prefix:
            raise Exception("Not available for new resources with prefix")
        lb_arn = element.get("values", {}).get("load_balancer_arn")
        if not lb_arn:
            raise MissingDependantObjectException(f"loadbalancer arn can't be calculated.")
        port = element.get("values", {}).get("port")
        protocol = element.get("values", {}).get("protocol")
        listeners = self.get_aws_client('elbv2', full_context, provider_config_key).describe_listeners(LoadBalancerArn=lb_arn)
        for listener in listeners["Listeners"]:
            if listener["Port"] == port and listener["Protocol"] == protocol:
                return listener["ListenerArn"]
        return None
