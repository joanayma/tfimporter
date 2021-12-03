from pprint import pprint
from typing import Dict, Any, Optional

from tfimporter import MissingDependantObjectException
from tfimporter.importers.aws import AwsImporter


class AwsLambdaEventSourceMappingImporter(AwsImporter):

    def __init__(self):
        super().__init__()
        self.description = 'AWS Lambda event source mapping'

    def supports_resource(self, resource_provider: str, resource_type: str) -> bool:
        return resource_provider == "registry.terraform.io/hashicorp/aws" and resource_type == "aws_lambda_event_source_mapping"

    def get_resource_id(self, element: Dict[str, Any], full_context: Dict[str, Any]) -> Optional[str]:

        provider_config_key = element.get("provider_config_key", "aws")
        function_name = element.get("values", {}).get("function_name")
        if not function_name:
            raise MissingDependantObjectException("Parent function not created yet")

        event_source_arn = element.get("values", {}).get("event_source_arn")
        if not event_source_arn:
            raise MissingDependantObjectException("Event source not created yet")

        for page in self.get_aws_client('lambda', full_context, provider_config_key).get_paginator('list_event_source_mappings').paginate(FunctionName=function_name, EventSourceArn=event_source_arn):
            for event_source_mapping_data in page.get("EventSourceMappings"):
                return event_source_mapping_data.get("UUID")

        return None
