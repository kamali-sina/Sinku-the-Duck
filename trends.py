import tweepy

def get_latest_trend(api):
    trends_result = api.trends_place(1)
    return trends_result[0]['trends'][0]
