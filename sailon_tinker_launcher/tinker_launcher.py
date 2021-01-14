"""Meta-configuration demonstration."""

import colorlog
import logging

from typing import Dict, Any

from tinker.protocol import Protocol
from sailon_tinker_launcher.main import LaunchSailonProtocol

log = logging.getLogger(__name__)


class TinkerLaunch(Protocol):
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

    def run_protocol(self, config: Dict[str, Any]) -> None:
        """Run the protocol
        """
        if 'defaults' in config.keys():
            del config['defaults']
        launch_protocol = LaunchSailonProtocol()
        self.config = config
        launch_protocol.run_protocol(config)



