from typing import List, Any
import twint
import tweepy
import datetime
import json


# TWEET CLASS
class Tweet:

    # constructor(s):
    def __init__(self, tweet_id=None, tweet_text=None, username=None, reply_id=None,
                 date=None, retweets=None, tweet_type=None, quoted_id=None,
                 referenced_tweet_id=None, conversation_id=None):
        self.tweet_id = tweet_id  # individ id
        self.tweet_text = tweet_text
        self.username = username
        self.reply_id = reply_id  # in_reply_to_status ID
        self.date = date
        self.retweets = retweets  # num of retweets
        self.tweet_type = tweet_type  # reply, root, quote
        self.quoted_id = quoted_id # id of quoted tweet
        self.referenced_tweet_id = referenced_tweet_id # id of referenced tweet, introduced in API v2
        self.conversation_id = conversation_id
        self.children = []  # list of children tweets

    # class method to search for tweet by id
    @classmethod
    def tweet_by_id(cls, tweetID: str, api: tweepy, backup_query=None):

        # try fromTweepy
        tweet = cls.fromTweepy(tweetID, api)
        if tweet:
            return tweet

        # try backup_query
        elif backup_query:
            tweet = backup_query(tweetID)
            if tweet:
                return tweet
            else:
                return None

        else:
            return None

    # method to create Tweet object from tweepy tweet
    @staticmethod
    def fromTweepy(tweetID: str, api: tweepy):

        # look up tweet from tweepy using tweet ID
        tweepyTweets = api.statuses_lookup([tweetID])

        # if search returns nothing
        if not tweepyTweets:
            return None
        else:
            tweepyTweet = tweepyTweets[0]
            # create Tweet object
            tweet = Tweet()
            tweet.tweet_id = tweepyTweet.id_str
            tweet.tweet_text = tweepyTweet.text
            tweet.username = tweepyTweet.user.screen_name
            tweet.reply_id = tweepyTweet.in_reply_to_status_id_str
            tweet.date = tweepyTweet.created_at
            tweet.retweets = tweepyTweet.retweet_count

            # tweet type
            if hasattr(tweepyTweet, 'quoted_status_id'):
                tweet.tweet_type = 'quote'
                tweet.quoted_id = tweepyTweet.quoted_status_id_str
            elif tweepyTweet.in_reply_to_status_id_str:
                tweet.tweet_type = 'reply'
            else:
                tweet.tweet_type = 'root'
            return tweet


    # to overload print function
    def __str__(self):
        return "Tweet ID: {0}\nText: {1}\nUsername: " \
               "{2}\nin_reply_to_status ID: {3}\ntweet_type: {4}".format(self.tweet_id,
                                                        self.tweet_text,
                                                        self.username,
                                                        self.reply_id,
                                                        self.tweet_type)

    # overloaded equality operator
    def __eq__(self, other):
        return self.tweet_id == other.tweet_id
