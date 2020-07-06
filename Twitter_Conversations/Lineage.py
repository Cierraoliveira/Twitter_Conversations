from typing import List
import twint
import tweepy
import datetime
from Twitter_Conversations.Tweet import Tweet


# LINEAGE CLASS
class Lineage:

    def __init__(self, leaf_tweet: Tweet = None, api: tweepy = None, backup_query=None):
        self.is_lineage_broken = False
        self.thread: List[Tweet] = []
        self.rootTweet = None
        # traverse if leaf_tweet is sent in
        if leaf_tweet and api:
            if backup_query:
                self.traverse(leaf_tweet, api, backup_query)
            else:
                self.traverse(leaf_tweet, api)

    # func to traverse lineages
    def traverse(self, current_tweet: Tweet, api: tweepy, backup_query=None):

        # add tweet to thread
        self.thread.append(current_tweet)

        # if reply
        if current_tweet.tweet_type == 'reply':

            # parent tweet from reply_id
            parent_tweet = Tweet().tweet_by_id(current_tweet.reply_id, api, backup_query)

            # if the lookup returns a tweet
            if parent_tweet:

                # recursively call traverse on parent tweet
                self.traverse(parent_tweet, api, backup_query)

            # if the lookup does not return a tweet
            else:
                self.is_lineage_broken = True

                # make dummy tweet with id and username
                deleted_parent = Tweet(tweet_id=current_tweet.reply_id, tweet_type='reply-deleted',
                                       username=api.statuses_lookup([current_tweet.tweet_id])[
                                           0].in_reply_to_screen_name,
                                       date=(current_tweet.date - datetime.timedelta(days=2)))
                self.thread.append(deleted_parent)

                # try to get root tweet
                root_attempt = self.get_broken_root(current_tweet, api, backup_query)
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
                        deleted_root = Tweet(tweet_id=conv_id, tweet_type='deleted')
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
    def get_broken_root(tweet: Tweet, api: tweepy, backup_query=None):
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
        root_tweet = Tweet().tweet_by_id(conv_id, api, backup_query)
        if root_tweet:
            root_tweet.tweet_type = 'root'
            return root_tweet
        else:
            return conv_id
