import requests

from Inteface.ISentimentAnalyzer import ISentimentAnalyzer
from Utilities.HttpUtility import SUCCESS

__author__ = 'Hannah'

# Constants
NEGATIVE_MIN = 0.9
API_ENDPOINT = "https://text-sentiment.p.mashape.com/analyze"
X_MASHAPE_KEY = ""
CONTENT_TYPE_HEADER = "application/x-www-form-urlencoded"
ACCEPT_HEADER = "application/json"
MAX_CALLS_PER_DAY = 1000

total_api_calls = 0


class MashapeSentimentAnalyzer(ISentimentAnalyzer):
    # Used to limit amount of calls per day
    total_api_calls = 0

    # Get raw results for comment from sentiment analyzer
    def get_raw_result(self, comment):

            # Make sure rate limit is not exceeded
            if self.total_api_calls == MAX_CALLS_PER_DAY:
                raise Exception('The max calls per day limit ({0}) has been exceeded!'.format(MAX_CALLS_PER_DAY))

            result = None

            # Prepare request headers
            headers = {
                "X-Mashape-Key": X_MASHAPE_KEY,
                "Content-Type": CONTENT_TYPE_HEADER,
                "Accept": ACCEPT_HEADER,
            }

            # Prepare request body
            body = {
                "text": comment.body
            }

            # Send request
            response = requests.post(API_ENDPOINT, headers=headers, data=body)
            self.total_api_calls += 1

            # Parse results of tone analysis
            if response.status_code == SUCCESS:
                result = response.json()

            return result

    # Determine if comment matches criteria
    def is_match(self, comment):

        match = False

        result = self.get_raw_result(comment)
        if None != result and \
            result["neg"] >= NEGATIVE_MIN:
            match = True

        return match


# class TestObj:
#     body = 'This is a test comment!'
#
#
# test = TestObj()
# sentiment_analyzer = MashapeSentimentAnalyzer()
# sentiment_analyzer.is_match(test)











