from pprint import pprint
from typing import Dict, Any, Optional

from tfimporter.importers.aws import AwsImporter


class AwsEcsTaskDefinitionImporter(AwsImporter):

    def __init__(self):
        super().__init__()
        self.description = 'AWS ECS Task Definition'

    def supports_resource(self, resource_provider: str, resource_type: str) -> bool:
        return resource_provider == "registry.terraform.io/hashicorp/aws" and resource_type == "aws_ecs_task_definition"

    def get_resource_id(self, element: Dict[str, Any], full_context: Dict[str, Any]) -> Optional[str]:
        provider_config_key = element.get("provider_config_key", "aws")
        family = element.get("values", {}).get("family")
        task_definitions = self.get_aws_client('ecs', full_context, provider_config_key).list_task_definitions(
            familyPrefix=family,status="ACTIVE")
        if len(task_definitions["taskDefinitionArns"]) > 1:
            raise Exception(f"too many ARN for active task definition family {family}")
        return task_definitions["taskDefinitionArns"][0]
