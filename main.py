import json
import os
import time
import praw
from praw.helpers import flatten_tree
from praw.objects import MoreComments
from Implementation.MashapeSentimentAnalyzer import MashapeSentimentAnalyzer


# Constants
DELIMITER = " "
SUBREDDIT = "askreddit"
SUBMISSION_LIMIT = 50
MIN_COMMENT_LENGTH = 200
MAX_TOP_LEVEL_COMMENTS = 25


# TODO: Modularize
def main():
    # Initialize sentiment analyzer
    sentiment_analyzer = MashapeSentimentAnalyzer()

    # Initialize connection to reddit API
    user_agent = "Percepto 0.1 by /u/_allocate"
    r = praw.Reddit(user_agent=user_agent)

    # Initialize logging info
    datetime = time.strftime("%Y-%m-%d_%H:%M")
    filename = "matches_{0}.txt".format(datetime)
    matches = []

    # Get hottest submissions in r/askreddit
    subreddit = r.get_subreddit(SUBREDDIT)
    for submission in subreddit.get_hot(limit=SUBMISSION_LIMIT):

        # Get top-level comments
        while len(submission.comments) < MAX_TOP_LEVEL_COMMENTS and \
                isinstance(submission.comments[-1], MoreComments):
            submission.replace_more_comments(limit=1)

        # Trim off extra top-level comments
        submission.comments = submission.comments[:MAX_TOP_LEVEL_COMMENTS]

        # Resolve remaining replies,
        # and flatten comment tree (hierarchy doesn't matter)
        submission.replace_more_comments(limit=None)
        all_comments = flatten_tree(submission.comments)

        debug_count = 0

        # Iterate through comments
        for comment in all_comments:

            # TODO: Refine this
            # Only process comment objects (not more comments)
            # if None != comment.body:

            # If suitable length, analyze comment
            word_count = comment.body.split(DELIMITER)
            debug_count += 1
            if len(word_count) >= MIN_COMMENT_LENGTH:

                # Determine if comment is match
                result = {}

                match = False
                try:
                    match = sentiment_analyzer.is_match(comment)
                except Exception as exception:
                    break

                # If match found, record it
                if match:
                    matches.append({
                        "comment": comment.__dict__,
                        "result": result
                    })

                    # Write to file
                    output = open(filename, "w+")
                    output.write(json.dumps(matches, indent=4, separators=(',', ': ')))
                    os.close(output)

main()