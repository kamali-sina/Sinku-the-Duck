import csv
import os
from random import random
from trends import get_latest_trend


MAIN_TWEETS_PATH = './tweets/main_tweets.csv'
REPEATABLE_TWEETS_PATH = './tweets/repeatable_tweets.csv'
REPLIES_PATH = './tweets/replies.csv'
TREND_PATH = './tweets/trend_tweets.csv'
PROMO_TREND_PATH = './tweets/promotional_trend_tweets.csv'
TWEET_RESETS = 3
T_TEXT = 0
T_MEDIA_BOOL = 1
T_MEDIA_PATH = 2
T_EXTRA = 3
TREND_FIND = '<###>'
FALSE_CSV = 'false'
TRUE_CSV = 'true'
SAVE_FILE = 'save_quack.txt'


def read_csv(csv_path):
    fields = []
    rows = []
    with open(csv_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        for row in csvreader:
            rows.append(row)
    return rows, fields


def get_random_index(lenght):
    return int(random() * lenght)



class Quacker:
    """
    Handles duck tweets!
    """

    main_tweets = None
    main_headers = None
    repeatable_tweets = None
    repeatable_headers = None
    replies = None
    replies_headers = None
    trends = None
    promo_trends = None
    main_tensor = []

    def __init__(self) -> None:
        self.main_tweets, self.main_headers = read_csv(MAIN_TWEETS_PATH)
        self.repeatable_tweets, self.repeatable_headers = read_csv(REPEATABLE_TWEETS_PATH)
        self.replies, self.replies_headers = read_csv(REPLIES_PATH)
        self.trends, _ = read_csv(TREND_PATH)
        self.promo_trends, _ = read_csv(PROMO_TREND_PATH)
        self.load_tweets_counter()
        self.make_main_tensor()
    
    def save(self):
        with open(SAVE_FILE, 'w') as save_file:
            save_file.write(str(self.tweets_counter) + "\n")

    def load_tweets_counter(self):
        if (not os.path.exists(SAVE_FILE)):
            self.tweets_counter = 0
            self.save()
            return
        with open(SAVE_FILE) as save_file:
            tweet_counter = int(save_file.readline())
            self.tweets_counter = tweet_counter

    def make_main_tensor(self):
        self.main_tensor = []
        for i in range(len(self.main_tweets)):
            if (self.main_tweets[i][T_EXTRA] == FALSE_CSV):
                self.main_tensor.append(i)
    
    def __tweet_line(self, api, line, in_reply_to=None):
        if (line[T_MEDIA_BOOL] == TRUE_CSV):
            media = api.media_upload(line[T_MEDIA_PATH])
            if (in_reply_to):
                api.update_status(status=line[T_TEXT],
                                    in_reply_to_status_id=in_reply_to,
                                    auto_populate_reply_metadata=True,
                                    media_ids=[media.media_id])
            else:
                api.update_status(status=line[T_TEXT],
                                    media_ids=[media.media_id])
        else:
            if (in_reply_to):
                api.update_status(status=line[T_TEXT],
                        in_reply_to_status_id=in_reply_to, auto_populate_reply_metadata=True)
            else:
                api.update_status(status=line[T_TEXT])
        print(f'tweeted tweeet:{line}')

    def quack(self, api):
        if (self.tweets_counter <= 0):
            self.tweets_counter = TWEET_RESETS
            self.post_main_tweet(api)
            self.save()
        else:
            if (self.tweets_counter % 2 == 1):
                self.post_repeatable_tweet(api)
            else:
                self.post_trend_tweet(api)
            self.tweets_counter -= 1
            self.save()
    
    def post_tweet_reply(self, api, in_reply_to_status_id):
        index = get_random_index(len(self.replies))
        self.__tweet_line(api, self.replies[index], 
                        in_reply_to=in_reply_to_status_id)

    def post_trend_tweet(self, api):
        trend = get_latest_trend(api)
        name = trend['name']
        is_promo = trend['promoted_content']
        line = ''
        if (not is_promo):
            index = get_random_index(len(self.trends))
            line = self.trends[index]
        else:
            index = get_random_index(len(self.promo_trends))
            line = self.promo_trends[index]
        line['T_TEXT'] = line[T_TEXT].replace(TREND_FIND, name)
        self.__tweet_line(api, line)

    def save_main_tweets(self):
        with open(MAIN_TWEETS_PATH, 'w') as main_tweets_file:
            main_tweets_file.write(','.join(self.main_headers) + "\n")
            for line in self.main_tweets:
                main_tweets_file.write(','.join(line) + "\n")
    
    def save_repeatable_tweets(self):
        with open(REPEATABLE_TWEETS_PATH, 'w') as repeatable_tweets_file:
            repeatable_tweets_file.write(','.join(self.repeatable_headers) + "\n")
            for line in self.repeatable_tweets:
                repeatable_tweets_file.write(','.join(line) + "\n")

    def restock_main_tweets(self):
        for line in self.main_tweets:
            line[T_EXTRA] = FALSE_CSV
        self.make_main_tensor()
        self.save_main_tweets()

    def post_main_tweet(self, api):
        if (len(self.main_tensor) == 0):
            self.restock_main_tweets()
        tensor_index = get_random_index(len(self.main_tensor))
        index = self.main_tensor[tensor_index]
        self.__tweet_line(api, self.main_tweets[index])
        self.main_tweets[index][T_EXTRA] = TRUE_CSV
        self.main_tensor.pop(tensor_index)
        self.save_main_tweets()
    
    def post_repeatable_tweet(self, api):
        index = get_random_index(len(self.repeatable_tweets))
        self.__tweet_line(api, self.repeatable_tweets[index])
        count = int(self.repeatable_tweets[index][T_EXTRA])
        self.repeatable_tweets[index][T_EXTRA] = str(count + 1)
        self.save_repeatable_tweets()
