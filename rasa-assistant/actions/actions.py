# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

import os
from langcodes import *
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from googleapiclient.discovery import build
import translators as ts

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
        keyword = tracker.get_slot('search_query')
        # get English equivalent of language name
        lang = ts.google(tracker.get_slot('lang'), to_language='en',if_use_cn_host=True)
        langcode = str(Language.find(lang))
        trans_keyword = ts.google(keyword, to_language=langcode,if_use_cn_host=True)

        request = youtube.search().list(
            part='snippet',
            q=trans_keyword,
            type='video',
            relevanceLanguage=langcode
        )

        response = request.execute()
        dispatcher.utter_message(text = '「%s」(%s)にとって%sで関連する５つのヒット：' % (keyword, trans_keyword, tracker.get_slot('lang')))
        for item in response['items']:
            id = item['id'].get('videoId')
            dispatcher.utter_message(text=youtube_url_base + id)

        return []

# This is a simple example for a custom action which utters "Hello World!"
# class ActionHelloWorld(Action):

#     def name(self) -> Text:
#         return "action_hello_world"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Hello World!")

#         return []
