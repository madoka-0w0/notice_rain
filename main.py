import settings
from schedule import Schedule
from slack_helper import Slack
from weather import WeatherClient
from datetime import datetime


def run():
    schedule = Schedule()
    manager = WeatherClient(settings.app_id(), settings.coordinates())
    slack = Slack(settings.slackurl())
    app = App()
    func = lambda: app.send_slack_if_rain(manager, slack)
    hour = 5 * 60

    schedule.start(interval=hour, func=func, wait=False)


class App:
    def __init__(self):
        self.send_slack = True

    def send_slack_if_rain(self, manager, slack):
        """
        If it can get 'weathers' have Rainfall data, it send message to slack url.

        :type manager: WeatherClient
        :type slack: Slack
        :return:
        """
        info = manager.get()
        weathers = info["Feature"][0]["Property"]["WeatherList"]["Weather"]
        rain_type = self.__is_raining(weathers)
        message = None
        if rain_type == "observation":
            message = "雨が降っています。"
        elif rain_type == "forecast":
            message = "雨が１時間以内に降るかもしれません。"

        if message is not None:
            if self.send_slack:
                slack.send(message)
                self.send_slack = False
        else:
            self.send_slack = True

    @staticmethod
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

        def __is_rainfall(weather):
            return weather["Rainfall"] != 0.0

        now = datetime.now()
        for weather in weathers:
            weather_type = weather["Type"]
            date = datetime.strptime(weather["Date"], "%Y%m%d%H%M")
            if weather_type == "observation" and (now - date).total_seconds() <= 10 * 60:
                if __is_rainfall(weather):
                    return weather_type
            elif weather_type == "forecast":
                if __is_rainfall(weather):
                    return weather_type


if __name__ == '__main__':
    run()
