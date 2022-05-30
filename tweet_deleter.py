'''
This script allows you to delete all your tweets, favorite tweets or both.
- Get tweepy ('pip3 install tweepy' https://www.tweepy.org/)
- Register a twitter application at http://dev.twitter.com to generate the  keys and tokens below.
'''

import time
import tweepy


CONSUMER_KEY = ''  # Also referred to as API Key
CONSUMER_SECRET = ''  # Also referred to as API Key Secret
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''


def limit_handler(cursor):
    '''This function handles twitter's api request limit'''
    try:
        while True:
            yield cursor.next()
    except tweepy.TooManyRequests:
        time.sleep(5)
    except StopIteration:
        return


def personal_tweets_deleter(personal):
    '''This function deletes all user's personal tweets'''
    for tweet in limit_handler(personal):
        try:
            api.destroy_status(tweet.id)
        except StopIteration:
            break
        except Exception as err:
            print('Failed to delete ID: ', tweet.id)
            raise err


def favorites_deleter(favorites):
    '''This function deletes all user's favorite tweets'''
    for tweet in limit_handler(favorites):
        try:
            api.destroy_favorite(tweet.id)
        except tweepy.errors.NotFound:
            break
        except StopIteration:
            break


if __name__ == '__main__':
    auth = tweepy.OAuth1UserHandler(
        CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
    )
    api = tweepy.API(auth)
    personal_tweets = tweepy.Cursor(api.user_timeline).items()
    favorite_tweets = tweepy.Cursor(api.get_favorites).items()
    action_prompt = input(
        'Would you like to delete your "tweets", "favorites" or "both"? ')
    while True:
        if action_prompt == 'tweets':
            personal_tweets_deleter(personal_tweets)
            print('All your tweets have been deleted.')
            break
        if action_prompt == 'favorites':
            favorites_deleter(favorite_tweets)
            print('All favorite tweets have been deleted.')
            break
        if action_prompt == 'both':
            favorites_deleter(favorite_tweets)
            personal_tweets_deleter(personal_tweets)
            print('All your favorite and personal tweets have been deleted.')
            break
        action_prompt = input(
            'Pleaser answer with "tweets", "favorites" or "both": ')
        continue
