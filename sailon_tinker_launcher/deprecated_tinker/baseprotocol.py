"""Base protocol class."""

import abc
import os
import sys
import inspect
import logging

from sailon_tinker_launcher.deprecated_tinker.basealgorithm import BaseAlgorithm
from sailon_tinker_launcher.deprecated_tinker.harness import Harness
from typing import Any, Dict

log = logging.getLogger(__name__)


class BaseProtocol(metaclass=abc.ABCMeta):
    """Provide generic toolset storage and mechanism to retrieve algorithms given their filename."""

    def __init__(
        self, discovered_plugins: Dict[str, Any], algodirectory: str, harness: Harness, config_file: str
    ) -> None:
        """
        Initialize.

        Arguments:
            discovered_plugins: A dictionary of plugin names and classes. Used to locate and instantiate
                                plugins
            algodirectory:      The path to the algorithms if they are located in a directory. This path
                                will be searched for algorithms first, and then a plugin will be loaded
                                if the path doe snot contain the named algorithm to be loaded.
            harness:            The interface to use for harness functionality (dataset access, test metadata,
                                etc...
            config_file:        The path to a configuration file for the protocol run.

        """
        self.test_harness = harness
        self.algorithmsbase = algodirectory
        self.discovered_plugins = discovered_plugins
        self.config_file = config_file
        self.toolset: Dict[str, Any] = {}

    @abc.abstractmethod
    def run_protocol(self) -> None:
        """Run the protocol."""
        raise NotImplementedError

    def get_algorithm(self, algotype: str, toolset: Dict[str, Any]) -> BaseAlgorithm:
        """
        Load a single algorithm file and instantiate the relevant object therefrom.

        Arguments:
            algotype: (option 1) This is a string that contains either an absolute or relative path to the
                        desired algorithm file. If the path is relative, then the location of
                        the file is determined using the self.algorithmsbase directory and
                        appending the algotype string to it to generate the absolute file path.

            algotype: (option 2) This is a string that names a plugin that has been pip installed. This
                        function will attempt to load using the plugin if a file with a matching name to
                        algotype can't be found.

            toolset: This is a dict() containing the initialization information for the algorithm.

        Returns:
            a single instantiated object of the desired algorithm class.
        """
        # load the algorithm from the self.algorithmsbase/algotype

        # TODO: implement the mechanism to override the normal behavior of this
        # function and use it to create template algorithm files and adapters
        # instead.

        # Validate the toolset is a dictionary or None
        if toolset and not isinstance(toolset, dict):
            log.error("toolset must be a dictionary")
            raise TypeError("toolset must be a dictionary")

        # if the file exists, then load the algo from the file. If not, then
        # load the algo from plugin
        algofile = os.path.join(self.algorithmsbase, algotype)
        if os.path.exists(algofile) and not os.path.isdir(algofile):
            log.info(f"{algotype} found in algorithms path, loading file")
            return self.load_from_file(algofile, toolset)
        else:
            log.info(f"{algotype} not found in path, looking for plugin now")
            return self.load_from_plugin(algotype, toolset)

    def load_from_file(self, algofile: str, toolset: Dict[str, Any]) -> BaseAlgorithm:
        """Load a protocol from a Python file."""

        # get the path to the algo file so that we can append it to the system path
        # this makes the import easier
        argpath, argfile = os.path.split(algofile)
        if argpath:
            sys.path.append(argpath)

        # load the file as a module and create an object of the class type in the file
        # the name of the class doesn't matter, as long as there is only one class in
        # the file.
        argbase, argext = os.path.splitext(argfile)
        if argext == ".py":
            algoimport = __import__(argbase, globals(), locals(), [], 0)
            for _name, obj in inspect.getmembers(algoimport):
                if inspect.isclass(obj):
                    foo = inspect.getmodule(obj)
                    if foo == algoimport:
                        # construct the algorithm object
                        algorithm = obj(toolset)
        else:
            log.error("Given algorithm is not a python file, other types not supported")
            raise AttributeError("Given algorithm is not a python file, other types not supported")

        return algorithm

    def load_from_plugin(self, algotype: str, toolset: Dict[str, Any]) -> BaseAlgorithm:
        """Load an algorithm from a plugin."""

        algorithm = self.discovered_plugins.get(algotype)
        if algorithm is None:
            log.error(f"Requested plugin not found '{algotype}'")
            raise AttributeError("Requested plugin not found")
        if not issubclass(algorithm, BaseAlgorithm):
            log.error(f"Requested plugin {algotype} is not an algorithm")
            raise AttributeError(f"Requested plugin {algotype} is not an algorithm")
        return algorithm(toolset)
