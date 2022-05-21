import praw #Python Reddit API Wrapper
import pandas as pd
from praw.models import MoreComments
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk import FreqDist
import emoji #remove emoji
import re #remove links
import en_core_web_sm
import spacy

class crawling_data():
    def __init__(self):
        print("Data Crawling Starts")
        self.user_agent = "Sentimental Analysus 1.0 by /u/alwayswhy98"
        self.reddit = praw.Reddit(client_id="",
                     client_secret="",
                     user_agent= self.user_agent)
        
        uncleaned_comments = self.obtain_comments()
        cleaned_comments = self.proprocess_comments(uncleaned_comments)
        
    def obtain_comments(self):
        for submission in self.reddit.subreddit("bitcoin").hot(limit=5):
            print(submission.title)
            print("Submission ID = ", submission.id, "\n")

        post1 = self.reddit.submission(id="uug57n")

        comments_all = []
        post1.comments.replace_more(limit=None)
        for comments in post1.comments.list():
            comments_all.append(comments.body)

        print(comments_all, "\n")
        print("Total Comments Scraped = ", len(comments_all))

        return comments_all

    def proprocess_comments(self, uncleaned_comments):
        #Convert to a string object
        string_list = [str(i) for i in uncleaned_comments]