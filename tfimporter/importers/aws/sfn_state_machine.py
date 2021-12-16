from pprint import pprint
from typing import Dict, Any, Optional

from tfimporter.importers.aws import AwsImporter


class AwsStepFunctionsImporter(AwsImporter):

    def __init__(self):
        super().__init__()
        self.description = 'AWS Step Functions'

    def supports_resource(self, resource_provider: str, resource_type: str) -> bool:
        return resource_provider == "registry.terraform.io/hashicorp/aws" and resource_type == "aws_sfn_state_machine"

    def get_resource_id(self, element: Dict[str, Any], full_context: Dict[str, Any]) -> Optional[str]:
        provider_config_key = element.get("provider_config_key", "aws")
        function_name = element.get("values", {}).get("name")
        step_functions = self.get_aws_client('stepfunctions', full_context, provider_config_key).list_state_machines()
        for sfn in step_functions["stateMachines"]:
            if sfn["name"] == function_name:
                return sfn["stateMachineArn"]
