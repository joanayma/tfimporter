from pprint import pprint
from typing import Dict, Any, Optional

from tfimporter.importers.aws import AwsImporter


class AwsLambdaFunctionImporter(AwsImporter):

    def __init__(self):
        super().__init__()
        self.description = 'AWS Lambda function'

    def supports_resource(self, resource_provider: str, resource_type: str) -> bool:
        return resource_provider == "registry.terraform.io/hashicorp/aws" and resource_type == "aws_lambda_permission"

    def get_resource_id(self, element: Dict[str, Any], full_context: Dict[str, Any]) -> Optional[str]:
        provider_config_key = element.get("provider_config_key", "aws")
        function_name = element.get("values", {}).get("function_name")
        statement_id = element.get("values", {}).get("statement_id")
        # boto3 query to lamba permissions not found
        return f"{function_name}/{statement_id}"
