from pprint import pprint
from typing import Dict, Any, Optional

from botocore.exceptions import ClientError

from tfimporter import ObjectNotFoundException
from tfimporter.importers.aws import AwsImporter


class AwsSqsQueueImporter(AwsImporter):

    def __init__(self):
        super().__init__()
        self.description = 'AWS SQS queue'

    def supports_resource(self, resource_provider: str, resource_type: str) -> bool:
        return resource_provider == "registry.terraform.io/hashicorp/aws" and resource_type == "aws_sqs_queue"

    def get_resource_id(self, element: Dict[str, Any], full_context: Dict[str, Any]) -> Optional[str]:

        provider_config_key = element.get("provider_config_key", "aws")
        name_prefix = element.get("values", {}).get("name_prefix")
        if name_prefix:
            raise Exception("Not available for new resources with prefix")

        queue_name = element.get("values", {}).get("name")
        try:
            return self.get_aws_client('sqs', full_context, provider_config_key).get_queue_url(QueueName=queue_name).get("QueueUrl")
        except ClientError as ex:
            if ex.response.get("Error", {}).get("Code") == "AWS.SimpleQueueService.NonExistentQueue":
                raise ObjectNotFoundException(queue_name)
            else:
                raise ex
