# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

import os
from langcodes import *
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from googleapiclient.discovery import build
from googletrans import Translator

youtube_api_key = os.environ.get('YT_API_KEY')
youtube_url_base = 'www.youtube.com/watch?v='

youtube = build('youtube', 'v3', developerKey=youtube_api_key)
translator = Translator()

class ActionGetYouTubeVideo(Action):

    def name(self) -> Text:

        return "action_get_youtube_vid"

    async def run(self,
                  dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        keyword = tracker.get_slot('search_query')
        lang = tracker.get_slot('lang')
        langcode = str(Language.find(lang))
        trans_keyword = translator.translate(keyword, dest=langcode).text

        request = youtube.search().list(
            part='snippet',
            q=trans_keyword,
            type='video',
            relevanceLanguage=langcode
        )

        response = request.execute()
        dispatcher.utter_message(text = 'Here are the top 5 search results for %s (%s) in %s.' % (keyword, trans_keyword, lang))
        for item in response['items']:
            id = item['id'].get('videoId')
            dispatcher.utter_message(text=youtube_url_base + id)

        return []
