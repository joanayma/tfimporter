from pprint import pprint
from typing import Dict, Any, Optional

from tfimporter.importers.aws import AwsImporter


class AwsSqsQueueImporter(AwsImporter):

    def __init__(self):
        super().__init__()
        self.description = 'AWS SQS queue'

    def supports_resource(self, resource_provider: str, resource_type: str) -> bool:
        return resource_provider == "aws" and resource_type == "aws_sqs_queue"

    def get_resource_id(self, resource_provider: str, resource_type: str, terraform_resource_name: str, terraform_values: Dict[str, Any], full_context: Dict[str, Any]) -> Optional[str]:

        name_prefix = terraform_values.get("name_prefix")
        if name_prefix:
            raise Exception("Not available for new resources with prefix")

        queue_name = terraform_values.get("name")
        return self.get_aws_client('sqs', full_context).get_queue_url(QueueName=queue_name).get("QueueUrl")
