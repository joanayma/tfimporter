#!/usr/bin/env python3.7
from abc import ABC, abstractmethod
import inspect
import os
import pkgutil
from typing import Any, Dict, Optional


class MissingDependantObjectException(Exception):
    pass


class Importer(ABC):
    """Base class that each plugin must inherit from. within this class
    you must define the methods that all of your plugins must implement.
    https://www.guidodiepen.nl/2019/02/implementing-a-simple-plugin-framework-in-python/
    """

    def __init__(self):
        super().__init__()
        self.description = 'UNKNOWN'

    @abstractmethod
    def supports_resource(self, resource_provider: str, resource_type: str) -> bool:
        pass

    @abstractmethod
    def get_resource_id(self, resource_provider: str, resource_type: str, terraform_resource_name: str, terraform_values: Dict[str, Any], full_context: Dict[str, Any]) -> Optional[str]:
        pass


class ImporterCollection(object):
    """Upon creation, this class will read the plugins package for modules
    that contain a class definition that is inheriting from the Plugin class
    """

    def __init__(self, plugin_package):
        """Constructor that initiates the reading of all available plugins
        when an instance of the PluginCollection object is created
        """
        self.plugins = []
        self.seen_paths = []
        self.plugin_package = plugin_package
        self.reload_plugins()

    def reload_plugins(self):
        """Reset the list of all plugins and initiate the walk over the main
        provided plugin package to load all available plugins
        """
        self.plugins = []
        self.seen_paths = []
        self.walk_package(self.plugin_package)

    def walk_package(self, package):
        """Recursively walk the supplied package to retrieve all plugins
        """
        imported_package = __import__(package, fromlist=['blah'])

        for _, plugin_name, is_package in pkgutil.iter_modules(imported_package.__path__, imported_package.__name__ + '.'):
            if not is_package:
                plugin_module = __import__(plugin_name, fromlist=['blah'])
                class_members = inspect.getmembers(plugin_module, inspect.isclass)
                for (_, c) in class_members:
                    # Only add classes that are a sub class of Plugin, but NOT Plugin itself
                    if issubclass(c, Importer) and (c is not Importer) and not inspect.isabstract(c):
                        self.plugins.append(c())

        # Now that we have looked at all the modules in the current package, start looking
        # recursively for additional modules in sub packages
        all_current_paths = []
        if isinstance(imported_package.__path__, str):
            all_current_paths.append(imported_package.__path__)
        else:
            all_current_paths.extend([x for x in imported_package.__path__])

        for pkg_path in all_current_paths:
            if pkg_path not in self.seen_paths:
                self.seen_paths.append(pkg_path)

                # Get all sub directory of the current package path directory
                child_packages = [p for p in os.listdir(pkg_path) if os.path.isdir(os.path.join(pkg_path, p))]

                # For each sub directory, apply the walk_package method recursively
                for child_package in child_packages:
                    self.walk_package(package + '.' + child_package)
