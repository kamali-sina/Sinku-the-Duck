import tweepy
import json

def get_api(credentials_path):
    with open(credentials_path) as json_file:
        credentials_data = json.load(json_file)
    auth = tweepy.OAuthHandler(credentials_data['api_key'], credentials_data['api_key_secret'])
    auth.set_access_token(credentials_data['token'], credentials_data['token_secret'])
    try:
        api = tweepy.API(auth)
        print('AUTH success!')
    except:
        print('AUTH failed!')
        exit()
    return api
