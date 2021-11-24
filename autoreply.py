import tweepy

def check_mentions(api, since_id, quacker):
    print('reading mentions...')
    since = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline, 
                                since_id=since_id).items():
        print(f'{tweet.user.name} replied:{tweet.text}')
        since = max(tweet.id, since)
        try:
            api.create_favorite(tweet.id)
            api.update_status(status="type duck message here",
                    in_reply_to_status_id=tweet.id)
        except:
            print('ERROR: can\'t like or tweet! help me!')
    return since