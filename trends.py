import tweepy

def get_latest_trend(api : tweepy.API):
    trends_result = api.get_place_trends(1)
    return trends_result[0]['trends'][1]
