from basket.utils.yaml import read_yaml_file


class Loss:
    def __init__(self, env, sim):
        self.env = env
        self.sim = sim

    def get_loss(self, tap_times: list[float]):
        raise NotImplementedError
