"""Meta-configuration demonstration."""

import colorlog
import logging
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Tuple
from pkg_resources import iter_entry_points, DistributionNotFound

from tinker.protocol import Protocol

from sail_on_client.protocol.condda_config import ConddaConfig
from sail_on_client.protocol.ond_config import OndConfig
from sail_on_client.protocol.condda import Condda
from sail_on_client.protocol.ond_protocol import SailOn as OND

from sail_on_client.protocol.localinterface import LocalInterface
from sail_on_client.protocol.parinterface import ParInterface
import sail_on_client.protocol as protocol_folder

log = logging.getLogger(__name__)


def discoverable_plugins() -> Dict[str, Any]:
    """
    Fixture to replicate plugin discovery from framework.
    """
    discovered_plugins = {}
    for entry_point in iter_entry_points("tinker"):
        try:
            ep = entry_point.load()
            discovered_plugins[entry_point.name] = ep
        except (DistributionNotFound, ImportError):
            logging.exception(f"Plugin {entry_point.name} not found")
    return discovered_plugins


class LaunchSailonProtocol(Protocol):
    """A protocol demonstrating how meta-configurations work."""

    def __init__(self) -> None:
        super().__init__()
        self.config = {}
        for handler in logging.getLogger().handlers:
            # For some reason isinstance doesn't work here but at least this does
            if handler.__class__ == logging.StreamHandler:
                handler.setFormatter(
                    colorlog.ColoredFormatter(
                        fmt='[%(cyan)s%(asctime)s%(reset)s][%(blue)s%(name)s%(reset)s]'
                            '[%(log_color)s%(levelname)s%(reset)s] - %(message)s',
                        log_colors={
                            'DEBUG': 'purple',
                            'INFO': 'green',
                            'WARNING': 'yellow',
                            'ERROR': 'red',
                            'CRITICAL': 'red,bg_white',
                        },
                    ),
                )
            else:
                handler.setFormatter(
                    fmt=logging.Formatter(
                        '[%(asctime)s][%(name)s][%(levelname)s] - %(message)s'
                    )
                )

    def get_config(self) -> Dict[str, Any]:
        """Return a default configuration dictionary."""
        return self.config

    @staticmethod
    def setup_experiment(config: Dict[str, Any]) -> Tuple[Path, Path, Dict[str, str], Dict[str, Any]]:
        """ Setup the folder and configuration for the experiment
        Steps involved in setup:
        - Delete the keys for this protocol and only pass on other parameters to sail-on protocols.
        - Validate config being sent to a protocol
        - hash the dictionary to create name of work folder and create the folder
        - save the config into the new folder

        Args:
            config: the configuration of the experiment

        """
        jconfig = json.dumps(config, indent=4)
        log.info('Running Config:')
        log.info(jconfig)

        # 1  Delete the keys for this protocol and only pass on other parameters.
        privileged_config = {'protocol': '', 'workdir': '', 'harness': ''}
        for pk in privileged_config.keys():
            if pk not in config:
                raise AttributeError(f'Please set "{pk}" in the config files')
            privileged_config[pk] = config[pk]
            del config[pk]

        # 2 Validate config being sent to a protocol.
        if privileged_config['protocol'] == 'condda':
            config = ConddaConfig(config).asdict()
        elif privileged_config['protocol'] == 'ond':
            config = OndConfig(config).asdict()
        else:
            raise AttributeError(f'Please set protocol to either "ond" or "condda".  '
                                 f'"{privileged_config["protocol"]}" in the config files')

        # 3 hash the dictionary to create temp name create the folder
        jconfig = json.dumps(config, indent=4)
        name = hashlib.blake2b(jconfig.encode('utf-8'), digest_size=10).hexdigest()

        log.info(f'Folder {name} created for the following config')
        working_folder = Path(privileged_config['workdir'], name).expanduser().resolve()
        working_folder.mkdir(exist_ok=True, parents=True)

        # 4 save the config into the new folder.
        working_config_fp = working_folder / 'config.json'
        with open(working_config_fp, 'w') as f:
            f.write(jconfig)
        log.debug(f'Config: \n{jconfig}')

        return working_folder, working_config_fp, privileged_config, config

    def run_protocol(self, config: Dict[str, Any]) -> None:
        """Run the protocol by printout out the config.
        Config passed in uses 3 parameters to control the launching of the protocols
            - protocol: either 'ond' or 'condda' to define which protocol to run
            - harness:  either 'local' or 'par' to define which harness to use
            - workdir: a directory to save all the information from the run including
                - Config
                - Output of algorithm

        TODO:
            - Update Results of Protocol to save to this new file.
            - Update any intermittent steps to this folder.
        """

        # Setup working folder and create new config for this run
        working_folder, working_config_fp, privileged_config, config = self.setup_experiment(config)
        self.config = config

        # Now experiment setup, start a new logger for this
        fh = logging.FileHandler(working_folder / f'{datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")}.log')
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s] - %(message)s')
        fh.setFormatter(formatter)
        logging.getLogger().addHandler(fh)
        log.info(f'Config Filepath: {working_config_fp}')
        log.info(f'Config: \n{json.dumps(config, indent=4)}')

        # Load the harness
        # This config is not used but will throw error if not pointed at
        harnness_config_path = Path(protocol_folder.__file__).parent
        if privileged_config['harness'] == 'local':
            log.debug('Loading Local Harness')
            harness = LocalInterface('configuration.json', harnness_config_path)
        elif privileged_config['harness'] == 'par':
            log.debug('Loading Par Harness')
            harness = ParInterface('configuration.json', harnness_config_path)
        else:
            raise AttributeError(f'Valid harnesses "local" or "par".  '
                                 f'Given harness "{privileged_config["harness"]}" ')

        # Get the plugins
        plugins = discoverable_plugins()
        log.debug('Plugins found:')
        log.debug(plugins)

        # Load the protocol
        if privileged_config['protocol'] == 'ond':
            log.info('Running OND Protocol')
            run_protocol = OND(discovered_plugins=plugins,
                           algorithmsdirectory='',
                           harness=harness,
                           config_file=str(working_config_fp))
        elif privileged_config['protocol'] == 'condda':
            log.info('Running Condda Protocol')
            run_protocol = Condda(discovered_plugins=plugins,
                              algorithmsdirectory='',
                              harness=harness,
                              config_file=str(working_config_fp))
        else:
            raise AttributeError(f'Please set protocol to either "ond" or "condda".  '
                                 f'"{privileged_config["protocol"]}" in the config files')

        # Run the protocol
        run_protocol.run_protocol()
        log.info('Protocol Finished')

        logging.getLogger().removeHandler(fh)
