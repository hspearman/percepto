import time
from django.contrib.sites import requests
from django.core.serializers import json
from requests.auth import HTTPBasicAuth
from Inteface.ISentimentAnalyzer import ISentimentAnalyzer
from Utilities.ConstantsUtility import API_RATE_LIMIT

__author__ = 'Hannah'

# IBM Bluemix credentials
API_RATE_LIMIT = 3
ANGER_THRESHOLD = 1
NEGATIVE_THRESHOLD = 1
credentials = {
    "url": "https://gateway.watsonplatform.net/tone-analyzer-experimental/api/v1/tone",
    "username": "",
    "password": ""
}

# Keeps track of when last API call made
last_api_call_timestamp = 0

class IbmSentimentAnalyzer(ISentimentAnalyzer):

    def is_match(self, comment, result):

        global last_api_call_timestamp
        match = False

        # Gather info for API call
        headers = {
            "Content-Type": "application/json"
        }
        payload = json.dumps({
            "text": comment.body
        })
        auth = HTTPBasicAuth(credentials["username"], credentials["password"])

        # Rate limit api calls
        since_last_api_call = time.time() - last_api_call_timestamp
        if since_last_api_call < API_RATE_LIMIT:
            remaining = API_RATE_LIMIT - since_last_api_call
            time.sleep(remaining)

        # Send API call
        last_api_call_timestamp = time.time()
        response = requests.post(credentials["url"], data=payload, headers=headers, auth=auth)

        # Parse results of tone analysis
        if response.status_code == 200:

            # Get scores
            result = response.json()
            scores = result["children"]

            # Get emotion scores
            emotion_scores = None
            for score in scores:
                if score["id"] == "emotion_tone":
                    emotion_scores = score

            # Get anger and negative scores in particular
            anger = [emotion for emotion in emotion_scores["children"] if emotion["id"] == "Anger"][0]
            negative = [emotion for emotion in emotion_scores["children"] if emotion["id"] == "Negative"][0]

            # If found match, record it
            match = anger["normalized_score"] >= ANGER_THRESHOLD and \
                    negative["normalized_score"] >= NEGATIVE_THRESHOLD

        return match