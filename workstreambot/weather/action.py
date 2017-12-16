from datetime import datetime
from network.yahooClient import YahooClient
from rasa_core.actions import Action

import json


class ActionSearchWeather(Action):
    # the name should match the action to the utterance
    def name(self):
        return 'action_search_weather'
    # the run executes when the action is called
    def run(self, dispatcher, tracker, domain):
        # get the location entity from the console
        location = tracker.get_slot('location')
        date = tracker.get_slot('time')
        # init the weather Client
        weatherClient = YahooClient()
        # fetch the weather data
        weather = weatherClient.fetch_weather_for_city(str(location))

        data = {}
        data['action_name'] = self.name()
        data['response'] = 'No data could be found.'


        if str(date) == "None":
           # get the weather factors
           description = weather.getWeatherDescription()
           condition = weather.getWeatherConditionFactors()
           conditionDesc = condition.getConditionDescription()
           conditionTemp = condition.getConditionCurrentTemperature()
           conditionDate = condition.getLastUpdatedConditionDate()

           data['response'] = description + '\nCondition: ' + conditionDesc + '\nThe currrent temperature is ' + conditionTemp + ' degree\nLast updated ' + conditionDate
           data['slots'] = tracker.current_slot_values()
        else:
           date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
           for num in range(0, len(weather.getWeatherForecastFactors())):
              forecast = weather.getWeatherForecastFactors()[num]
              if date.strftime('%d %b %Y') == forecast.getLastUpdatedForecastDate():
                 # get the weather factors
                 description = weather.getWeatherDescription()
                 forecastDesc = forecast.getForecastDescription()
                 forecastHigh = forecast.getForecastHighTemperature()
                 forecastLow = forecast.getForecastLowTemperature()
                 forecastDate = forecast.getLastUpdatedForecastDate()

                 data['response'] = description + ' on ' + forecastDate + '\nCondition: ' + forecastDesc + '\nThe temperature is between ' + forecastLow + ' and ' + forecastHigh + ' degree'
                 data['slots'] = tracker.current_slot_values()

        dispatcher.utter_message(json.dumps(data))
        return []


class ActionGreet(Action):
    def name(self):
        return 'utter_greet'

    def run(self, dispatcher, tracker, domain):
        data = {}
        data['action_name'] = self.name()

        data['response'] = 'Hey there!'
        data['slots'] = tracker.current_slot_values()

        dispatcher.utter_message(json.dumps(data))
        return []


class ActionGoodbye(Action):
    def name(self):
        return 'utter_goodbye'

    def run(self, dispatcher, tracker, domain):
        data = {}
        data['action_name'] = self.name()

        data['response'] = 'Aloha'
        data['slots'] = tracker.current_slot_values()

        dispatcher.utter_message(json.dumps(data))
        return []


class ActionAskHowCanIHelp(Action):
    def name(self):
        return 'utter_ask_howcanhelp'

    def run(self, dispatcher, tracker, domain):
        data = {}
        data['action_name'] = self.name()

        data['response'] = 'How can I help you?'
        data['slots'] = tracker.current_slot_values()

        dispatcher.utter_message(json.dumps(data))
        return []


class ActionOnIt(Action):
    def name(self):
        return 'utter_on_it'

    def run(self, dispatcher, tracker, domain):
        data = {}
        data['action_name'] = self.name()

        data['response'] = "I'm on it!"
        data['slots'] = tracker.current_slot_values()

        dispatcher.utter_message(json.dumps(data))
        return []


class ActionAskLocation(Action):
    def name(self):
        return 'utter_ask_location'

    def run(self, dispatcher, tracker, domain):
        data = {}
        data['action_name'] = self.name()

        data['response'] = "Please enter the city you're interested in."
        data['slots'] = tracker.current_slot_values()

        dispatcher.utter_message(json.dumps(data))
        return []


class ActionAckDoSearch(Action):
    def name(self):
        return 'utter_ack_dosearch'

    def run(self, dispatcher, tracker, domain):
        data = {}
        data['action_name'] = self.name()

        data['response'] = "Ok let me see what I can find."
        data['slots'] = tracker.current_slot_values()

        dispatcher.utter_message(json.dumps(data))
        return []


class ActionAskHelpMore(Action):
    def name(self):
        return 'utter_ask_helpmore'

    def run(self, dispatcher, tracker, domain):
        data = {}
        data['action_name'] = self.name()

        data['response'] = "Is there anything more that I can help with?"
        data['slots'] = tracker.current_slot_values()

        dispatcher.utter_message(json.dumps(data))
        return []
