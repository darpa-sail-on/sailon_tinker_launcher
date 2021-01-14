import hydra
from omegaconf import DictConfig, OmegaConf
from sailon_tinker_launcher.main import LaunchSailonProtocol


@hydra.main(config_name="config")
def hydra_launcher(cfg: DictConfig) -> None:
    launch_protocol = LaunchSailonProtocol()
    launch_protocol.run_protocol(OmegaConf.to_container(cfg))


if __name__ == "__main__":
    hydra_launcher()
