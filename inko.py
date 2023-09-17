import taipy as tp
from taipy.core.config import Config

Config.load('my_config.toml')

scenario_cfg = Config.scenarios['scenario']

if __name__ == '__main__':
    tp.Core().run()

    scenario_1 = tp.create_scenario(scenario_cfg)
    print("submitting")

    scenario_1.submit()
    print("submit shit ayyindhi")
