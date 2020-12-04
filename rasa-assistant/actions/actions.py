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
import rasa.core.channels.console

import translators as ts
from youtube_search import YoutubeSearch

rasa.core.channels.console.DEFAULT_STREAM_READING_TIMEOUT_IN_SECONDS = 25
YOUTUBE_URL_BASE = "https://www.youtube.com"

class ActionGetYouTubeVideo(Action):

    def name(self) -> Text:

        return "action_get_youtube_vid"

    async def run(self,
                  dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        keyword = tracker.get_slot('search_query')
        lang = tracker.get_slot('lang')
        print("checkpoint 1")
        langcode = str(Language.find(lang))
        print("checkpoint 2")
        trans_keyword = ts.bing(keyword, to_language=langcode,if_use_cn_host=False)	
        print("checkpoint 3")
        results = YoutubeSearch(trans_keyword, max_results=5).to_dict()
        print("checkpoint 4")

        dispatcher.utter_message(text = 'Here are the top 5 search results for %s (%s) in %s.' % (keyword, trans_keyword, lang))
        for item in results:
            id = item['url_suffix']
            dispatcher.utter_message(text=YOUTUBE_URL_BASE + id)
        print("checkpoint 5")
        return []

# class ActionHelloWorld(Action):

#     def name(self) -> Text:
#         return "action_hello_world"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Hello World!")

#         return []
