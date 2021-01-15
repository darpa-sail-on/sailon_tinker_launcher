import hydra
from omegaconf import DictConfig, OmegaConf
from sailon_tinker_launcher.main import LaunchSailonProtocol
import logging

log = logging.getLogger(__name__)


@hydra.main(config_name="config")
def hydra_launcher(cfg: DictConfig) -> None:
    """ Load the protocol and then run it

    """
    launch_protocol = LaunchSailonProtocol()
    launch_protocol.run_protocol(OmegaConf.to_container(cfg))


if __name__ == "__main__":
    hydra_launcher()
