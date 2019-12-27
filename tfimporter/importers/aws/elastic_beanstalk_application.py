from pprint import pprint
from typing import Dict, Any, Optional

from tfimporter.importers.aws import AwsImporter


class AwsElasticBeanstalkApplicationImporter(AwsImporter):

    def __init__(self):
        super().__init__()
        self.description = 'AWS Elastic Beanstalk application'

    def supports_resource(self, resource_provider: str, resource_type: str) -> bool:
        return resource_provider == "aws" and resource_type == "aws_elastic_beanstalk_application"

    def get_resource_id(self, resource_provider: str, resource_type: str, terraform_resource_name: str, terraform_values: Dict[str, Any], full_context: Dict[str, Any]) -> Optional[str]:
        application_name = terraform_values.get("name")
        return self.get_aws_client('elasticbeanstalk', full_context).describe_applications(ApplicationNames=[application_name]).get("Applications")[0].get("ApplicationName")
