import os
import argparse
from basket.env import load_env_from_yaml
from basket.sim import SymplecticEulerSimulator
from basket.loss import load_loss_from_yaml
from basket.optimizer import load_optimizer_from_yaml
from basket.ui import TaichiUI
from Play_setting import PlaySetting
from test_opt_air_fric import test_opt_air

if __name__ == '__main__':
    mode = PlaySetting()
    test_opt_air()