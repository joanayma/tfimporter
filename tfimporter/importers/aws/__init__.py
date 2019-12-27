from abc import ABC
from pprint import pprint
from typing import Dict, Any

import boto3

from tfimporter import Importer


class AwsImporter(Importer, ABC):

    @staticmethod
    def get_aws_client(service_name: str, full_context: Dict[str, Any]):

        aws_provider_config = full_context.get("configuration", {}).get("provider_config", {}).get("aws", {}).get("expressions", {})
        region_name = aws_provider_config.get("region", {}).get("constant_value")
        profile_name = aws_provider_config.get("profile", {}).get("constant_value")
        aws_access_key_id = aws_provider_config.get("access_key", {}).get("constant_value")
        aws_secret_access_key = aws_provider_config.get("secret_key", {}).get("constant_value")
        aws_session_token = aws_provider_config.get("token", {}).get("constant_value")

        session = boto3.Session(
            profile_name=profile_name,
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
        )

        return session.client(
            service_name=service_name
        )
