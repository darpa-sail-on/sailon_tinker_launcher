import hydra
from omegaconf import DictConfig, OmegaConf
from sailon_tinker_launcher.main import LaunchSailonProtocol
import logging

log = logging.getLogger(__name__)


@hydra.main(config_path="configs", config_name="h_config")
def hydra_launcher(cfg: DictConfig) -> None:
    """ Load the protocol and then run it

    """
    log.info(cfg)
    launch_protocol = LaunchSailonProtocol()
    launch_protocol.run_protocol(OmegaConf.to_container(cfg['problem']))


if __name__ == "__main__":
    hydra_launcher()
