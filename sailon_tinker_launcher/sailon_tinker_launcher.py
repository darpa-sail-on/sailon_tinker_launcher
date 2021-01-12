"""Meta-configuration demonstration."""

from tinker import protocol
import colorlog
import logging
import json
import hashlib
from pathlib import Path
from pkg_resources import iter_entry_points, DistributionNotFound

from sail_on_client.protocol.condda_config import ConddaConfig
from sail_on_client.protocol.ond_config import OndConfig
from sail_on_client.protocol.condda import Condda
from sail_on_client.protocol.ond_protocol import SailOn as OND

from sail_on_client.protocol.localinterface import LocalInterface
from sail_on_client.protocol.parinterface import ParInterface
import sail_on_client.protocol as protocol_folder

log = logging.getLogger(__name__)


def discoverable_plugins():
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


# def combine_configs(base_config, config):
#     for key, val in config.items():
#
#
#
#     return base_config


class ShowConfig(protocol.Protocol):
    """A protocol demonstrating how meta-configurations work."""

    def __init__(self):
        for handler in logging.getLogger().handlers:
            handler.setFormatter(colorlog.ColoredFormatter('%(log_color)s%(levelname)s:%(name)s:%(message)s'))

    def get_config(self):
        """Return a default configuration dictionary."""
        return {}

    @staticmethod
    def setup_experiment(config):
        """ Setup the folder and configuration for the experiment

        Args:
            config: the configuration of the experiment

        """

        # 1   Delete the keys for this protocol and only pass on other parameters.

        jconfig = json.dumps(config, indent=4)
        log.info('Running Config:')
        log.info(jconfig)

        # Remove the Metaprotocol config items
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
        log.info(jconfig)
        working_folder = Path(privileged_config['workdir'], name).expanduser().resolve()
        working_folder.mkdir(exist_ok=True, parents=True)

        # 5 save the config into the new folder.
        working_config_fp = working_folder / 'config.json'
        with open(working_config_fp, 'w') as f:
            f.write(jconfig)
        log.debug(f'Config Filepath: {working_config_fp}')
        log.debug(f'Config{jconfig}')

        return working_folder, working_config_fp, privileged_config, config

    def run_protocol(self, config):
        """Run the protocol by printout out the config."""

        # Setup working folder
        working_folder, working_config_fp, privileged_config, config = self.setup_experiment(config)

        # 2 Setup inputs for
        log.info(working_config_fp)
        # Load the harness

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

        plugins = discoverable_plugins()
        log.debug('Plugins found:')
        log.debug(plugins)

        if privileged_config['protocol'] == 'ond':
            log.info('Running OND Protocol')
            protocol = OND(discovered_plugins=plugins,
                           algorithmsdirectory='',
                           harness=harness,
                           config_file=working_config_fp)
        elif privileged_config['protocol'] == 'condda':
            log.info('Running Condda Protocol')
            protocol = Condda(discovered_plugins=plugins,
                              algorithmsdirectory='',
                              harness=harness,
                              config_file=working_config_fp)
        else:
            raise AttributeError(f'Please set protocol to either "ond" or "condda".  '
                                 f'"{privileged_config["protocol"]}" in the config files')

        # Run the protocol

        protocol.run_protocol()

        log.info('Protocol Finished')
