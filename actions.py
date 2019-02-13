# -*- coding: utf-8 -*-
import requests
import json
from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet

class ActionJoke(Action):
    def name(self):
        # type: () -> Text
        return "action.ActionJoke"

    def run(self, dispatcher, tracker, domain):
        # what your action should do
        request = json.loads(requests.get('https://api.chucknorris.io/jokes/random').text)  # make an api call
        # joke = {'text': request['value']} # extract a joke from returned json response
        # dispatcher.utter_message(request['value'])  # send the message back to the user
        dispatcher.utter_message(request['value'])
        return []
