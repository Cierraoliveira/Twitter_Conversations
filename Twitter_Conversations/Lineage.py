from typing import List
import twint
import tweepy
import datetime
from Twitter_Conversations.Tweet import Tweet


# LINEAGE CLASS
class Lineage:

    def __init__(self, leaf_tweet: Tweet = None, api: tweepy = None):
        self.is_lineage_broken = False
        self.thread: List[Tweet] = []
        # list of tweets in thread
        self.rootTweet = None
        # traverse if leaf_tweet is sent in
        if leaf_tweet and api:
            self.traverse(leaf_tweet, api)

    # func to traverse lineages
    def traverse(self, current_tweet: Tweet, api: tweepy):

        # add tweet to thread
        self.thread.append(current_tweet)

        # if reply
        if current_tweet.tweet_type == 'reply':

            # parent tweet from reply_id
            parent_tweet = Tweet().fromTweepy(current_tweet.reply_id, api)

            # if the lookup returns a tweet
            if parent_tweet:

                # recursively call traverse on parent tweet
                self.traverse(parent_tweet, api)

            # if the lookup does not return a tweet
            else:
                self.is_lineage_broken = True
                self.rootTweet = self.get_broken_root(current_tweet, api)
                current_tweet.tweet_type = 'broken_head'

        # if quote
        elif current_tweet.tweet_type == 'quote':
            parent_tweet = Tweet().fromTweepy(current_tweet.quoted_id, api)

            if parent_tweet:
                self.traverse(parent_tweet, api)

        # if root
        else:
            self.rootTweet = current_tweet

    # func to get root from broken thread
    @staticmethod
    def get_broken_root(tweet: Tweet, api: tweepy):
        leaf_tweet = []

        # grab conversation id from twint
        c = twint.Config()
        c.Username = tweet.username
        c.Search = tweet.tweet_text
        c.Since = str(tweet.date - datetime.timedelta(days=1))
        c.Until = str(tweet.date + datetime.timedelta(days=1))
        c.Hide_output = True
        c.Store_object = True
        c.Store_object_tweets_list = leaf_tweet
        twint.run.Search(c)

        # check that only 1 tweet is found
        # assert len(leaf_tweet) <= 1, "More than one tweet found."

        conv_id = str(leaf_tweet[0].conversation_id)

        # create Tweet object from Tweepy using conversation ID
        root_tweet = Tweet().fromTweepy(conv_id, api)
        return root_tweet
