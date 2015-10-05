import requests

from Inteface.ISentimentAnalyzer import ISentimentAnalyzer
from Utilities.HttpUtility import SUCCESS

__author__ = 'Hannah'

POSITIVE_MAX = 10
NEGATIVE_MIN = 90

# Constants
OPERATION = "ClassifyUrl"
API_ENDPOINT = "http://uclassify.com/browse/{0}/{1}/{2}",
CLASSIFIER_NAME = "sentiment"
REMOVE_HTML = True
OUTPUT_TYPE = "json"
MAX_CALLS_PER_DAY = 1000
COMMENT_DEPTH = 1

credentials = {
    "username": "",
    "readkey": ""
}

total_api_calls = 0

class ClassifySentimentAnalyzer(ISentimentAnalyzer):
    # Used to limit amount of calls per day
    total_api_calls = 0

    # Get raw results for comment from sentiment analyzer
    def get_raw_result(self, comment):

            result = None

            # Prepare query params
            query_params ={
                "readkey": credentials["readkey"],
                "removeHtml": REMOVE_HTML,
                "output": OUTPUT_TYPE,
                "url": comment.permalink # TODO: Add depth
            }

            # Prepare url
            api_endpoint = API_ENDPOINT.format(
                credentials["username"],
                CLASSIFIER_NAME,
                OPERATION
            )

            # Send request
            response = requests.get(api_endpoint, params=query_params)
            self.total_api_calls += 1

            # Parse results of tone analysis
            if response.status_code == SUCCESS:
                result = response.json()

            return result

    # Determine if comment matches criteria
    def is_match(self, comment):

        match = False

        result = self.get_raw_result(comment)
        # if None != result:
        #     match = process_raw_result(result)

        return match

    # Process raw result to determine if match was found
    # def process_raw_result(self, result):
    #
    #     results = result["call_id"]
    #     if (result["negative"]):









