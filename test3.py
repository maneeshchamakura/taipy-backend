from taipy import Config
from functions import build_message




name_data_node_cfg = Config.configure_data_node(id="name")
message_data_node_cfg = Config.configure_data_node(id="message")
build_msg_task_cfg = Config.configure_task("build_msg", build_message, name_data_node_cfg, message_data_node_cfg)
scenario_cfg = Config.configure_scenario_from_tasks("scenario", task_configs=[build_msg_task_cfg])

Config.export('my_config.toml')