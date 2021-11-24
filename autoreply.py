import tweepy

def check_mentions(api, since_id):
    print('reading mentions...')
    since = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline, 
                                since_id=since_id).items():
        since = max(tweet.id, since)
        api.create_favorite(tweet.id)
        api.update_status(status="type duck message here", 
                in_reply_to_status_id=tweet.id)
        return since