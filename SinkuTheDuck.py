from time import time
import tweepy
import json
from config import get_api

with open('credentials.json') as json_file:
    credentials_data = json.load(json_file)

auth = tweepy.OAuthHandler(credentials_data['api_key'], credentials_data['api_key_secret'])
auth.set_access_token(credentials_data['token'], credentials_data['token_secret'])

try:
    api = tweepy.API(auth)
    print('AUTH success!')
except:
    print('wtf?')
    exit()

# timeline = api.home_timeline()

# api.update_status("Hello world, Sinku the duck is here!")

class SinkuTheDuck:
    api = None

    def __init__(self, credentials_path='credentials.json'):
        self.api = get_api

    # def get_top_trend_name(self):