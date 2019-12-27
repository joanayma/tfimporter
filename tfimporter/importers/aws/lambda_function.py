from pprint import pprint
from typing import Dict, Any, Optional

from tfimporter.importers.aws import AwsImporter


class AwsLambdaFunctionImporter(AwsImporter):

    def __init__(self):
        super().__init__()
        self.description = 'AWS Lambda function'

    def supports_resource(self, resource_provider: str, resource_type: str) -> bool:
        return resource_provider == "aws" and resource_type == "aws_lambda_function"

    def get_resource_id(self, resource_provider: str, resource_type: str, terraform_resource_name: str, terraform_values: Dict[str, Any], full_context: Dict[str, Any]) -> Optional[str]:
        function_name = terraform_values.get("function_name")
        return self.get_aws_client('lambda', full_context).get_function(FunctionName=function_name).get("Configuration").get("FunctionName")
