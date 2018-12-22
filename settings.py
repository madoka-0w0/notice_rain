import os

import yaml

filepath = os.path.join(os.path.curdir, "config", "settings.yml")


def __get_setting():
    with open(filepath, encoding="utf-8")as f:
        return yaml.load(f)


def app_id():
    return __get_setting()["YOLP"]["appid"]


def coordinates():
    return __get_setting()["coordinates"]


def slackurl():
    return __get_setting()["slack"]["url"]
