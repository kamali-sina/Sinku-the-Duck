from os import read
import tweepy
import csv

MAIN_TWEETS_PATH = './tweets/main_tweets.csv'
REPEATABLE_TWEETS_PATH = './tweets/repeatable_tweets.csv'
REPLIES_PATH = './tweets/replies.csv'
TWEET_RESETS = 3

def read_csv(csv_path):
    fields = []
    rows = []
    with open(csv_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        for row in csvreader:
            rows.append(row)
    return rows

"""
    Handles duck tweets!
"""
class Quacker:
    main_tweets = None
    repeatable_tweets = None
    replies = None

    def __init__(self) -> None:
        self.main_tweets = read_csv(MAIN_TWEETS_PATH)
        self.repeatable_tweets = read_csv(REPEATABLE_TWEETS_PATH)
        self.replies = read_csv(REPLIES_PATH)
        self.tweets_counter = 0
    
    def quack(self, api):
        if (self.tweets_counter <= 0):
            self.tweets_counter = TWEET_RESETS
            self.post_main_tweet(api)
        else:
            self.main_tweets -= 1
            self.post_repeatble_tweet(api)
    
    def post_tweet_reply(self, api, in_reply_to_status_id):
        # TODO:
        pass

    def post_main_tweet(self, api):
        # TODO:
        pass
    
    def post_repeatble_tweet(self, api):
        # TODO:
        pass


Quacker()