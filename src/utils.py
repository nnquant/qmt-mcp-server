import os
import yaml


def _new_config():
    config = {
        "path": input("请输入MiniQMT所在路径 (userdata_mini): "),
        "account_id": input("请输入资金账户: ")
    }
    return config


def load_config():
    if not os.path.exists("xttrader.yaml"):
        config = _new_config()
        with open("xttrader.yaml", "w", encoding="utf-8") as f:
            yaml.dump(config, f)
        return config
    else:
        with open("xttrader.yaml", "r", encoding="utf-8") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        return config
