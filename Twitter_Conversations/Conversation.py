from typing import List
import twint
import tweepy
import datetime
from Twitter_Conversations.Tweet import Tweet
from Twitter_Conversations.Lineage import Lineage


# CONVERSATION CLASS
class Conversation:

    # constructor
    def __init__(self, lineage: Lineage = None, api: tweepy = None):
        self.tree: List[Tweet] = []  # list of all tweets in conversation
        self.size = len(self.tree)  # number of tweets in conversation
        # fillTree if rootTweet is sent in
        if lineage and api:
            self.fillTree(lineage, api)

    # func to fill out conversation
    def fillTree(self, lineage: Lineage, api: tweepy):

        # add rootTweet to tree
        self.tree.append(lineage.rootTweet)

        # add broken leafs
        if lineage.is_lineage_broken:
            for i in lineage.thread:
                self.tree.append(i)  # add to conv tree
            # add most recent broken tweet to root tweet
            self.tree[0].children.append(lineage.thread[-1])

            # for the size of the conversation
        for N in self.tree:

            # search for tweets addressed to N
            addressedTweets = self.search_addressed(N)  # list of addressed tweets

            # for all the addressed tweets found from twint
            for j in range(len(addressedTweets)):
                # hydrate with reply_id from tweepy
                foundReply = Tweet().fromTweepy(addressedTweets[j].id, api)

                # if the reply id matches the parent tweet's id and not already in tree
                if foundReply.reply_id == N.tweet_id and foundReply not in self.tree:
                    self.tree.append(foundReply)  # append to conv tree
                    N.children.append(foundReply)  # append to tweet children

            # search for quoted tweets
            quotedTweets = self.search_quotes(N)  # list of quoted tweets

            for k in range(len(quotedTweets)):
                foundQuote = Tweet().fromTweepy(quotedTweets[k].id, api)
                if foundQuote not in self.tree:
                    self.tree.append(foundQuote)  # add quote to conv tree
                    N.children.append(foundQuote)  # add quote to tweet children

    # query twint for tweets addressed to user
    @staticmethod
    def search_addressed(tweet: Tweet):
        addressedTweets = []  # list of addressed tweets
        q = 'to:' + tweet.username
        c = twint.Config()
        c.Search = q
        c.Since = str(tweet.date - datetime.timedelta(days=1))
        c.Until = str(tweet.date + datetime.timedelta(days=21))
        c.Store_object = True
        c.Store_object_tweets_list = addressedTweets
        c.Hide_output = True
        twint.run.Search(c)
        return addressedTweets

    # query twint for quoted tweets
    @staticmethod
    def search_quotes(tweet: Tweet):
        # construct url
        url1 = 'https://twitter.com/' + tweet.username + '/status/' + tweet.tweet_id
        url2 = 'https://twitter.com/' + tweet.username.lower() + '/status/' + tweet.tweet_id
        # search twint for tweets with containing url
        quotedTweets = []  # list of quoted tweets
        c = twint.Config()
        c.Search = url1 + ' OR ' + url2
        c.Store_object = True
        c.Store_object_tweets_list = quotedTweets
        c.Hide_output = True
        twint.run.Search(c)
        return quotedTweets
