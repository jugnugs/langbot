# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import os
from langcodes import *
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from googleapiclient.discovery import build

youtube_api_key = os.environ.get('YT_API_KEY')
youtube_url_base = 'www.youtube.com/watch?v='

youtube = build('youtube', 'v3', developerKey=youtube_api_key)

class ActionGetYouTubeVideo(Action):

    def name(self) -> Text:

        return "action_get_youtube_vid"

    async def run(self,
                  dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # keyword = tracker.get_slot('search_query')
        # lang = tracker.get_slot('lang')
        # langcode = str(Language.find(lang))
        keyword = 'among us'
        lang = 'English'
        langcode = str(Language.find(lang))

        request = youtube.search().list(
            part='snippet',
            q=keyword,
            relevanceLanguage=langcode
        )
        response = request.execute()

        for item in response['items']:
            id = item['id']['videoId']
            # dispatcher.utter_message(text = youtube_url_base + id)
            print(youtube_url_base + id)

        return []


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []
