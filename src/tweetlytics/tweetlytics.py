# Authors: Mahsa Sarafrazi, Mahmood Rahman, Shiva Shankar Jena, Amir Shojakhani
# Jan 2022

# imports
from arrow import now
import requests
import os
import json
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import re
from collections import Counter
from string import punctuation

load_dotenv()  # load .env files in the project folder

def get_store(
    bearer_token,
    keyword,
    start_date,
    end_date,
    max_results=25,
    store_path="output/",
    store_csv=False,
    include_public_metrics=True,
    api_access_lvl="essential",
):
    """
    Retreives all tweets of a keyword provided by the user through the Twitter API.
    Alternatively the user can directly read from a structered Json response based
    on the Twitter API.
    If the user plans to access to the Twitter API they must have a personal bearer
    token and store it as an environement variable to access it.
    Parameters:
    -----------
    bearer_token : string
        The user's personal twitter API dev bearer token.
        It is recommended to add the token from an
        enviroment variable.
    keyword : string
        The keyword to search Twitter and retrieve tweets.
    start_date: string
        Starting date to collect tweets from. Dates should be
        entered in string format: YYYY-MM-DD
    end_date: string
        Ending date (Included) to collect tweets from. Dates should be
        entered in string format: YYYY-MM-DD
    max_results: int
        The maximum number of tweets to return. Default is 25.
        Must be between 10 and 100.
    store_path: string
        The string path to store the retrieved tweets in
        Json format. Default is working directory.
    store_csv: boolean
        Create .csv file with response data or not.
        Default is False.
    include_public_metrics : boolean
        Should public metrics regarding each tweet such as
        impression_count, like_count, reply_count, retweet_count,
        url_link_clicks and user_profile_clicks be downloaded
        and stored. Default is True.
    api_access_lvl : string
        The twitter API access level of the user's bearer token.
        Options are 'essential' or 'academic'.
        Default is 'essential'
    Returns:
    --------
    tweets_df : dataframe
        A pandas dataframe of retrieved tweets based on user's
        selected parameters. (Data will be stored as a Json file)
    Examples
    --------
    >>> bearer_token = os.getenv("BEARER_TOKEN")
    >>> tweets = get_store(
            bearer_token,
            keyword="vancouver",
            start_date="2022-01-12",
            end_date="2022-01-17")
    >>> tweets
    """

    # parameter tests
    if not isinstance(bearer_token, str):
        raise TypeError(
            "Invalid parameter input type: bearer_token must be entered as a string"
        )
    if not isinstance(keyword, str):
        raise TypeError(
            "Invalid parameter input type: keyword must be entered as a string"
        )
    if not isinstance(start_date, str):
        raise TypeError(
            "Invalid parameter input type: start_date must be entered as a string"
        )
    if not (
        datetime.strptime(end_date, "%Y-%m-%d")
        > datetime.strptime(start_date, "%Y-%m-%d")
        > (datetime.now() - timedelta(days=7))
    ) & (api_access_lvl == "essential"):
        raise ValueError(
            "Invalid parameter input value: api access level of essential can only search for tweets in the past 7 days"
        )
    if not isinstance(end_date, str):
        raise TypeError(
            "Invalid parameter input type: end_date must be entered as a string"
        )
    if not (
        datetime.now()
        >= datetime.strptime(end_date, "%Y-%m-%d")
        > datetime.strptime(start_date, "%Y-%m-%d")
    ):
        raise ValueError(
            "Invalid parameter input value: end date must be in the range of the start date and today"
        )
    if not isinstance(max_results, int):
        raise TypeError(
            "Invalid parameter input type: max_results must be entered as an integer"
        )
    if not isinstance(store_path, str):
        raise TypeError(
            "Invalid parameter input type: store_path must be entered as a string"
        )
    if not isinstance(store_csv, bool):
        raise TypeError(
            "Invalid parameter input type: store_csv must be entered as a boolean"
        )
    if not api_access_lvl in ["essential", "academic"]:
        raise ValueError(
            "Invalid parameter input value: api_access_lvl must be of either string essential or academic"
        )

    headers = {
        "Authorization": "Bearer {}".format(bearer_token)
    }  # set authorization header for API

    # check access level and switch url accordingly. recent will can only search the past 7 days.
    if api_access_lvl == "essential":
        search_url = "https://api.twitter.com/2/tweets/search/recent"
    elif api_access_lvl == "academic":
        search_url = "https://api.twitter.com/2/tweets/search/all"

    # set request parameters
    query_params = {
        "query": f"{keyword}",
        "start_time": f"{start_date}T00:00:00.000Z",
        "end_time": f"{end_date}T00:00:00.000Z",
        "max_results": f"{max_results}",
        "expansions": "author_id,in_reply_to_user_id",
        "tweet.fields": "id,text,author_id,in_reply_to_user_id,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source",
        "user.fields": "id,name,username,created_at,description,public_metrics,verified,entities",
        "place.fields": "full_name,id,country,country_code,name,place_type",
        "next_token": {},
    }

    # send request and store response
    tweet_response = requests.request(
        "GET", search_url, params=query_params, headers=headers
    )
    tweet_response_json = tweet_response.json()

    # check if path in store path exists. create folders if not and create .Json file
    if not os.path.exists(store_path):
        os.makedirs(store_path)
    with open(os.path.join(store_path, "tweets_response.json"), "w") as file:
        json.dump(tweet_response_json, file, indent=4, sort_keys=True)

    tweets_df = pd.DataFrame.from_dict(tweet_response_json["data"])

    # expand public_metrics column and store in separate columns.
    tweets_df[["retweetcount", "reply_count", "like_count", "quote_count"]] = tweets_df[
        "public_metrics"
    ].apply(pd.Series)

    if store_csv:
        tweets_df.to_csv(os.path.join(store_path, "tweets_response.csv"), index=False)

    return tweets_df


def clean_tweets(file_path, tokenization=True, word_count=True):
    """
    Cleans the text in the tweets and returns as new columns in the dataframe.
    
    The cleaning process includes converting into lower case, removal of punctuation, hastags and hastag counts
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
        
 