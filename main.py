import settings
from schedule import Schedule
from slack_helper import Slack
from weather import WeatherClient


def run():
    schedule = Schedule()
    manager = WeatherClient(settings.app_id(), settings.coordinates())
    slack = Slack(settings.slackurl())
    func = lambda: send_slack_if_rain(manager, slack)
    hour = 60 * 60

    schedule.start(interval=hour, func=func, wait=False)


def send_slack_if_rain(manager, slack):
    """
    If it can get 'weathers' have Rainfall data, it send message to slack url.

    :type manager: WeatherClient
    :type slack: Slack
    :return:
    """
    info = manager.get()
    weathers = info["Feature"][0]["Property"]["WeatherList"]["Weather"]
    rain_type = __is_raining(weathers)
    message = None
    if rain_type == "observation":
        message = "雨が降っています。"
    elif rain_type == "forecast":
        message = "雨が１時間以内に降るかもしれません。"
    if message is not None:
        slack.send(message)


def __is_raining(weathers):
    """
    If 'weathers' have Rainfall data, return weather Type. (ex. "observation" or "forecast")

    :param weathers:
    [{
        "Type": "observation" or "forecast"
        "Date": "201812221850"
        "Railfall": 10.00 * not need
    }]
    :type weathers: list[dict[str,any]]
    :return: "observation" or "forecast" or None
    """
    for weather in weathers:
        rainfall = weather.get("Rainfall")
        if rainfall is not None:
            return weather["Type"]


if __name__ == '__main__':
    run()
