from pprint import pprint
from typing import Dict, Any, Optional

from tfimporter import MissingDependantObjectException, NoOpException
from tfimporter.importers.aws import AwsImporter


class AwsSecurityGroupRuleImporter(AwsImporter):

    def __init__(self):
        super().__init__()
        self.description = 'AWS security group rule'

    def supports_resource(self, resource_provider: str, resource_type: str) -> bool:
        return resource_provider == "registry.terraform.io/hashicorp/aws" and resource_type == "aws_security_group_rule"

    def get_resource_id(self, element: Dict[str, Any], full_context: Dict[str, Any]) -> Optional[str]:
        provider_config_key = element.get("provider_config_key", "aws")
        values = element.get("values")
        security_group_id = values.get("security_group_id")
        if not security_group_id:
            raise MissingDependantObjectException("Parent security group not imported or created yet")
        rule_type = values.get("type")
        protocol = values.get("protocol")
        from_port = values.get("from_port")
        to_port = values.get("to_port")
        rule_self = values.get("self")
        cidr_blocks = values.get("cidr_blocks")
        prefix_list_ids = values.get("prefix_list_ids")
        source_sg = values.get("source_security_group_id")
        import_string = "_".join([
            security_group_id,
            rule_type,
            str(protocol),
            str(from_port),
            str(to_port)
        ])
        if rule_self:
            import_string += "_self"
        if cidr_blocks:
            import_string += "_" + "_".join(cidr_blocks)
        if prefix_list_ids:
            import_string += "_" + "_".join(prefix_list_ids)
        if source_sg:
            import_string += "_" + source_sg
        return import_string
