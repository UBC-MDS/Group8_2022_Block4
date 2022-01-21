# Authors: Mahsa Sarafrazi, Mahmood Rahman, Shiva Shankar Jena, Amir Shojakhani
# Jan 2022

# imports
import requests
import os
from pathlib import Path
import json
import pandas as pd
from dotenv import load_dotenv
import re
from collections import Counter
from string import punctuation

load_dotenv()  # load .env files in the project folder


def clean_tweets(file_path, tokenization=True, word_count=True):
    """
    Cleans the text in the tweets and returns as new columns in the dataframe.

    The function cleans the raw tweets text removing Reference Tweets 
    (RTs @usernames),converts the raw tweets into lowercase, cleans the hashtags, 
    mentions, punctuations and non-alphanumerics, and returns new columns in the
    dataframe containing cleaned tweets, tokens and word count.

    Parameters:
    -----------
    file_path : string
        File path to csv file containing tweets data
    tokenization : Boolean
        Creates new column containing cleaned tweet word tokens when True
        Default is True
    word_count : Boolean
        Creates new column containing word count of cleaned tweets
        Default is True

    Returns:
    --------
    df : pandas dataframe
        A dataframe comprising tweets data after cleaning raw text

    Examples
    --------
    >>> tweet_df = clean_tweets("output/tweets_response.csv")
    """
    # Checking for valid input parameters
    if not isinstance(file_path, str):
        raise Exception("'input_file' must be of str type")
    if not isinstance(tokenization, bool):
        raise Exception("'tokenization' must be of bool type")
    if not isinstance(word_count, bool):
        raise Exception("'word_count' must be of bool type")
    
    # Dropping irrelavant columns
    columns=["public_metrics"]
    df = pd.read_csv(file_path).drop(columns=columns)
    
    # Checking for 'df' to be a dataframe
    if not isinstance(df, pd.DataFrame):
        raise Exception("'df' must be of DataFrame type.")
    
    # Looping through the data set 
    for i in range(len(df)):
        # Cleaning a retweet tag 'RT @xx:'
        tweet_text = df.loc[i,"text"]
        tweet_text = re.sub(r"RT\s@.*:\s","",tweet_text)

        # Lowercasing
        tweet_text.lower()

        # Cleaning hashtags and mentions in tweet
        tweet_text = re.sub(r"@[A-Za-z0-9_]+","", tweet_text)
        tweet_text = re.sub(r"#[A-Za-z0-9_]+","", tweet_text)

        # Cleaning links
        tweet_text = re.sub(r"http\S+", "", tweet_text)
        tweet_text = re.sub(r"www.\S+", "", tweet_text)

        # Cleaning all punctuations and non-alpha numerics
        tweet_text = tweet_text.strip(punctuation).replace(",", "")

        # Adding clean_tweets column    
        df.loc[i, "clean_tweets"] = tweet_text

        # Adding clean_tokens column
        if tokenization:
            df.loc[i, "clean_tokens"] = ','.join(tweet_text.split())
        
        # Adding word_count column
        if word_count:
            df.loc[i, "word_count"] = len(tweet_text.split())
         
    return df
        
 