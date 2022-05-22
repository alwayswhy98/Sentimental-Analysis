from distutils.command.clean import clean
import praw #Python Reddit API Wrapper
import pandas as pd
from praw.models import MoreComments
import nltk
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
        print("Original length of words: ", len(uncleaned_comments))
        print("Preprocessed length or words: ", cleaned_comments)
        
    def obtain_comments(self):
        posts_id = []
        for submission in self.reddit.subreddit("bitcoin").hot(limit=5):
            print(submission.title)
            print("Submission ID = ", submission.id, "\n")
            posts_id.append(submission.id)

        comments_all = []
        for id in posts_id:
            post = self.reddit.submission(id=id)
            post.comments.replace_more(limit=None)
            for comments in post.comments.list():
                comments_all.append(comments.body)

        print(comments_all, "\n")
        print("Total Comments Scraped = ", len(comments_all))

        return comments_all

    def proprocess_comments(self, uncleaned_comments):
        #Convert to a string object
        string_list = [str(i) for i in uncleaned_comments]
        string_uncleaned = " , ".join(string_list)
        #Removing Emijis
        string_emojiless = emoji.get_emoji_regexp().sub(u'', string_uncleaned)
        #Tokenizing & Cleaning String
        tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|http\S+')
        tokenized_string = tokenizer.tokenize(string_emojiless)
        #Converting tokens into lowercase
        lower_string_tokenized = [word.lower() for word in tokenized_string]
        #Remove stopwords
        nlp = en_core_web_sm.load()
        all_stopwords = nlp.Defaults.stop_words
        text = lower_string_tokenized
        tokens_without_sw = [word for word in text if not word in all_stopwords]
        #Normalizing words via Lemmatizing
        nltk.download('wordnet')
        lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = ([lemmatizer.lemmatize(w) for w in tokens_without_sw])

        return lemmatized_tokens
