import requests

class WeatherApiCall():
    def __init__(self, user_search):
        self.base_url = "http://api.weatherapi.com/v1/"
        self.api_key = ""
        self.user_search = user_search
        self.parameter = {
            "key": self.api_key,
            "q": self.user_search
        }

    def current_weather(self):
        self.url = self.base_url + "/current.json"
        return self.make_request(self.url, self.parameter)

    def forecast_weather(self):

        self.url = self.base_url + "/forecast.json"
        days = input("How many days would you like to see? Max is 14 days: ")
        self.parameter['days'] = days

        return self.make_request(self.url, self.parameter)

    def history_weather(self):
        pass

    def make_request(self, url, parameter):

        try:
            call = requests.get(url=url, params=parameter)
            return call.json()

        except Exception as e:
            print(f"Error {e}")



location = input("Please enter what city and state you would like to look up. ex. Los Angeles, CA: ")

weather = WeatherApiCall(location)
print(weather.forecast_weather())
