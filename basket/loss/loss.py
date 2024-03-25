from basket.utils.yaml import read_yaml_file

class Loss:
    def __init__(self, env, sim, loss_options=None, loss_options_path=None):
        self.env = env
        self.sim = sim

        if loss_options is not None:
            self.loss_options = loss_options
        elif loss_options_path is not None:
            yaml_content = read_yaml_file(loss_options_path)
            self.loss_options = yaml_content['loss']

    def get_loss(self, tap_times: list[float]):
        raise NotImplementedError
