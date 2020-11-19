from typing import List
import twint
import tweepy
import datetime
import requests
from Twitter_Conversations.Tweet import Tweet


# LINEAGE CLASS
class Lineage:

    def __init__(self, leaf_tweet: Tweet = None, api: tweepy = None, backup_query=None, headers=None):
        self.is_lineage_broken = False
        self.thread: List[Tweet] = []
        self.rootTweet = None
        # traverse if leaf_tweet is sent in
        if leaf_tweet and api:
            if headers:
                self.traverse(leaf_tweet, api, headers=headers)
            else:
                self.traverse(leaf_tweet, api)

    # func to traverse lineages
    def traverse(self, current_tweet: Tweet, api: tweepy, backup_query=None, headers=None):

        # add tweet to thread
        self.thread.append(current_tweet)

        # if reply
        if current_tweet.tweet_type == 'reply':

            # parent tweet from reply_id
            parent_tweet = Tweet().tweet_by_id(current_tweet.reply_id, api, backup_query)

            # if the lookup returns a tweet
            if parent_tweet:

                # recursively call traverse on parent tweet
                self.traverse(parent_tweet, api, backup_query, headers)

            # if the lookup does not return a tweet
            else:
                self.is_lineage_broken = True

                # make dummy tweet with id and username
                deleted_parent = Tweet(tweet_id=current_tweet.reply_id, tweet_type='reply-deleted')
                self.thread.append(deleted_parent)

                # try to get root tweet
                root_attempt = self.get_broken_root(current_tweet, api, backup_query, headers)
                # if search returns root
                if type(root_attempt) == Tweet:
                    self.rootTweet = root_attempt
                    self.thread.append(root_attempt)
                else:
                    conv_id = root_attempt
                    # if deleted tweet is root tweet
                    if conv_id == deleted_parent.tweet_id:
                        self.rootTweet = deleted_parent
                        deleted_parent.tweet_type = 'root-deleted'
                    # if not, create dummy root tweet without username
                    else:
                        deleted_root = Tweet(tweet_id=conv_id, tweet_type='root-deleted')
                        self.thread.append(deleted_root)

        # if quote
        elif current_tweet.tweet_type == 'quote':
            parent_tweet = Tweet().tweet_by_id(current_tweet.quoted_id, api, backup_query)

            if parent_tweet:
                self.traverse(parent_tweet, api, backup_query)
            else:
                self.is_lineage_broken = True
                # make dummy tweet with id
                deleted_tweet = Tweet(tweet_id=current_tweet.quoted_id, tweet_type='deleted')
                self.thread.append(deleted_tweet)

        # if root
        else:
            self.rootTweet = current_tweet

    # func to get root from broken thread
    @staticmethod
    def get_broken_root(tweet: Tweet, api: tweepy, backup_query, headers):

        # attempt to get conversation id from tweet
        if tweet.conversation_id:
            conv_id = tweet.conversation_id
        # attempt to get conversation id from twitter api if headers is sent in
        elif headers:
            tweet_fields = "tweet.fields=conversation_id"
            current_id = tweet.tweet_id
            url = "https://api.twitter.com/2/tweets/{}?{}".format(current_id,tweet_fields)
            response = (requests.request("GET", url, headers=headers)).json()

            if 'data' in response:
                conv_id = response['data']['conversation_id']
            # return none if you cannot grab conversation id
            else:
                return None
        else:
            return None

        # create Tweet object from Tweepy using conversation ID
        root_tweet = Tweet().tweet_by_id(conv_id, api, backup_query)
        if root_tweet:
            root_tweet.tweet_type = 'root'
            return root_tweet

        # if the root tweet is deleted, return the conversation id
        else:
            return conv_id
