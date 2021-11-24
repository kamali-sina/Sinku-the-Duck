from time import time, sleep
import tweepy
import os
import json
from config import get_api
from autoreply import check_mentions
from Quacker import Quacker

TIME_BETWEEN_TWEETS = 6 * 60 * 60 # 12 hours

class SinkuTheDuck:
    api = None
    last_tweet_time = 0
    since_id = 1
    quacker = None

    def __init__(self, credentials_path='credentials.json'):
        self.api = get_api(credentials_path)
        self.quacker = Quacker()
        self.load()

    def save(self):
        with open('save.txt', 'w') as save_file:
            save_file.write(str(self.last_tweet_time) + "\n")
            save_file.write(str(self.since_id) + "\n")

    def post_tweet(self):
        self.quacker.quack(self.api)
        pass

    def check_mentions(self):
        self.since_id = check_mentions(self.api, self.since_id, self.quacker)
        self.save()

    def load(self):
        if (not os.path.exists('save.txt')):
            self.last_tweet_time = int(time())
            tweet = self.api.user_timeline(screen_name = 'SinkuTheDuck', count = 1)[0]
            self.since_id = tweet.id
            self.save()
            self.post_tweet()
            return
        with open('save.txt') as save_file:
            timestamp = int(save_file.readline())
            since = int(save_file.readline())
            self.last_tweet_time = timestamp
            self.since_id = since
    
    def update_last_tweet_time(self, new_time):
        self.last_tweet_time = new_time
        self.save()

    def run(self):
        while(1):
            if (time() - self.last_tweet_time > TIME_BETWEEN_TWEETS):
                self.update_last_tweet_time(int(time()))
                self.post_tweet()
            self.check_mentions()
            sleep(60)
            



s = SinkuTheDuck()
s.run()