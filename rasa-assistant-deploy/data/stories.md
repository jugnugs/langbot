## ask about use happy path
* greet
  - utter_greet_start
* ask_uses
  - utter_uses
* affirm
  - utter_planned_features
  - utter_did_that_help
* affirm
  - utter_happy
* goodbye
  - utter_goodbye

## youtube search form happy path
* request_youtube_vid
    - utter_prompt_youtube_form
    - youtube_vid_form
    - form{"name": "youtube_vid_form"}
    - form{"name": null}
    - action_get_youtube_vid

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot
