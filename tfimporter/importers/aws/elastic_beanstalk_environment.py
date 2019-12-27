from pprint import pprint
from typing import Dict, Any, Optional

from tfimporter import MissingDependantObjectException
from tfimporter.importers.aws import AwsImporter


class AwsElasticBeanstalkEnvironmentImporter(AwsImporter):

    def __init__(self):
        super().__init__()
        self.description = 'AWS Elastic Beanstalk environment'

    def supports_resource(self, resource_provider: str, resource_type: str) -> bool:
        return resource_provider == "aws" and resource_type == "aws_elastic_beanstalk_environment"

    def get_resource_id(self, resource_provider: str, resource_type: str, terraform_resource_name: str, terraform_values: Dict[str, Any], full_context: Dict[str, Any]) -> Optional[str]:

        application_name = terraform_values.get("application")
        if not application_name:
            raise MissingDependantObjectException("Parent application not created yet")

        environment_name = terraform_values.get("name")
        for page in self.get_aws_client('elasticbeanstalk', full_context).get_paginator('describe_environments').paginate(ApplicationName=application_name, EnvironmentNames=[environment_name]):
            for environment_data in page.get("Environments"):
                return environment_data.get("EnvironmentId")

        return None
