class Vis:
    def __init__(self,
                 env=None,
                 bounds=None,
                 ball_radius=None,
                 basket_radius=None,
                 basket_ring_radius=None,
                 board_width=None,
                 board_height=None):
        if env:
            self.bounds = env.bounds
            self.ball_radius = env.ball_radius
            self.basket_radius = env.basket_radius
            self.basket_ring_radius = env.basket_ring_radius
            self.board_width = env.board_width
            self.board_height = env.board_height
            self.default_env = env
        else:
            self.bounds = bounds
            self.ball_radius = ball_radius
            self.basket_radius = basket_radius
            self.basket_ring_radius = basket_ring_radius
            self.board_width = board_width
            self.board_height = board_height
            self.default_env = None

    def add_trajectory(self, sim, env=None):
        raise NotImplementedError

    def show(self):
        raise NotImplementedError

    def save_file(self, filename):
        raise NotImplementedError
