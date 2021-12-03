import argparse
import json
import logging
import os
import subprocess
import sys
import tempfile
from nested_lookup import nested_lookup
from pprint import pprint

import colorama

from tfimporter import ImporterCollection, MissingDependantObjectException, ObjectNotFoundException

INFO = colorama.Fore.CYAN
SUCCESS = colorama.Fore.GREEN
MODIFIED = colorama.Fore.MAGENTA
WARNING = colorama.Fore.YELLOW
ERROR = colorama.Fore.RED


class ColorPrint(object):

    def __init__(self, no_color: bool):
        self.no_color = no_color

    def color_print(self, message: str, color: str, prefix: str):
        if self.no_color:
            print(prefix.ljust(12, ".") + " " + message)
        else:
            print(color + prefix.ljust(12, ".") + " " + message + colorama.Style.RESET_ALL)

    def info(self, message: str):
        self.color_print(message, INFO, "INFO")

    def skipped(self, message: str):
        self.color_print(message, INFO, "SKIPPED")

    def already_present(self, message: str):
        self.color_print(message, SUCCESS, "PRESENT")

    def imported(self, message: str):
        self.color_print(message, MODIFIED, "IMPORTED")

    def warning(self, message: str):
        self.color_print(message, WARNING, "WARNING")

    def missing(self, message: str):
        self.color_print(message, WARNING, "MISSING")

    def error(self, message: str):
        self.color_print(message, ERROR, "ERROR")

    def not_found(self, message: str):
        self.color_print(message, ERROR, "NOT_FOUND")


def main(terraform_path: str, save_state: bool, no_color: bool) -> int:

    color_print = ColorPrint(no_color)

    color_print.info("Loading workspace...")
    result = subprocess.run(["terraform", "workspace", "show"], cwd=terraform_path, capture_output=True, universal_newlines=True)
    if result.returncode:
        color_print.error(f"Error loading workspace ({result.returncode}): {result.stderr}")
        return 1

    workspace = result.stdout.split("\n")[0]
    color_print.info(f"Current workspace is {workspace}")

    plan_file_fd, plan_file_name = tempfile.mkstemp()

    color_print.info("Generating plan...")
    result = subprocess.run(["terraform", "plan", "-out", plan_file_name], cwd=terraform_path, capture_output=True, universal_newlines=True)
    if result.returncode:
        os.unlink(plan_file_name)
        color_print.error(f"Error generating Terraform plan ({result.returncode}): {result.stderr}")
        return 1

    color_print.info("Converting plan to JSON...")
    result = subprocess.run(["terraform", "show", "-json", plan_file_name], cwd=terraform_path, capture_output=True, universal_newlines=True)
    os.unlink(plan_file_name)
    if result.returncode:
        color_print.error(f"Error converting Terraform plan to JSON ({result.returncode}): {result.stderr}")
        return 1

    configuration = json.loads("".join(result.stdout))

    color_print.info("Loading state...")
    result = subprocess.run(["terraform", "state", "list"], cwd=terraform_path, capture_output=True, universal_newlines=True)
    if result.returncode:
        if "No state file was found!" in result.stderr:
            # Ignore this error, no state has been set yet
            existing_state_resources = {}
        else:
            color_print.error(f"Error loading state ({result.returncode}): {result.stderr}")
            return 1
    else:
        existing_state_resources = [x for x in result.stdout.split("\n") if x]

    importers = ImporterCollection('tfimporter.importers')

    all_resources = [x for x in configuration.get("planned_values", {}).get("root_module", {}).get("resources", {}) if x.get("mode") == "managed"]
    for modules in nested_lookup("child_modules", configuration):
        for module in modules:
            for resource in module.get("resources", []):
                if resource.get("mode") == "managed":
                    all_resources.append(resource)


    for idx, element in enumerate(all_resources):
        address = element.get("address")
        provider_name = element.get("provider_name")
        provider_config_key = element.get("provider_config_key", "aws")
        element_type = element.get("type")
        element_tf_name = element.get("name")
        values = element.get("values") or {}

        if address in existing_state_resources:
            color_print.already_present(f"{address}: already in state")
            continue

        name_prefix = values.get("name_prefix")
        if name_prefix:
            color_print.skipped(f"{address}: resource defined with name_prefix ({name_prefix})")
            continue

        for importer in importers.plugins:

            if importer.supports_resource(provider_name, element_type):
                try:
                    resource_id = importer.get_resource_id(provider_name, element_type, element_tf_name, values, configuration)
                    if resource_id:
                        if save_state:
                            try:

                                result = subprocess.run(["terraform", "import", address, resource_id], cwd=terraform_path, capture_output=True, universal_newlines=True)
                                if result.returncode:
                                    color_print.error(f"{address}: error importing state ({result.returncode}): {result.stderr}")
                                else:
                                    color_print.imported(f"{address}: saved state (external ID: {resource_id})")

                                # Reload state after save
                                result = subprocess.run(["terraform", "state", "list"], cwd=terraform_path, capture_output=True, universal_newlines=True)
                                if result.returncode:
                                    if "No state file was found!" in result.stderr:
                                        # Ignore this error, no state has been set yet
                                        existing_state_resources = {}
                                    else:
                                        color_print.error(f"Error reloading state ({result.returncode}): {result.stderr}")
                                        return 1

                            except Exception as ex:
                                color_print.error(f"{address}: error saving state: {str(ex)}")
                        else:
                            color_print.missing(f"{address}: external ID is {resource_id}")
                    else:
                        color_print.warning(f"{address}: no external ID guessed")
                except MissingDependantObjectException as ex:
                    color_print.error(f"{address}: missing dependant object: {str(ex)}")
                except ObjectNotFoundException as ex:
                    color_print.not_found(f"{address}: object not found ({str(ex)})")
                except Exception as ex:
                    color_print.error(f"{address}: error getting external ID: {str(ex)}")
                break

        else:
            color_print.error(f"{address}: unknown element type, skipping")

    return 0


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--save', action='store_true', help="Save state")
    parser.add_argument('--no-color', action='store_true', help="Disable console colors")
    parser.add_argument('terraform_path', default=".")
    args = parser.parse_args()

    if not args.no_color:
        colorama.init()

    sys.exit(main(args.terraform_path, args.save, args.no_color))
