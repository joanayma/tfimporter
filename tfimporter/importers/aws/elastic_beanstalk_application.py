from pprint import pprint
from typing import Dict, Any, Optional

from tfimporter.importers.aws import AwsImporter


class AwsElasticBeanstalkApplicationImporter(AwsImporter):

    def __init__(self):
        super().__init__()
        self.description = 'AWS Elastic Beanstalk application'

    def supports_resource(self, resource_provider: str, resource_type: str) -> bool:
        return resource_provider == "registry.terraform.io/hashicorp/aws" and resource_type == "aws_elastic_beanstalk_application"

    def get_resource_id(self, element: Dict[str, Any], full_context: Dict[str, Any]) -> Optional[str]:
        provider_config_key = element.get("provider_config_key", "aws")
        application_name = element.get("values", {}).get("name")
        return self.get_aws_client('elasticbeanstalk', full_context, provider_config_key).describe_applications(ApplicationNames=[application_name]).get("Applications")[0].get("ApplicationName")
