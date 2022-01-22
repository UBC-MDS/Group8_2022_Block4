# Authors: Mahsa Sarafrazi, Mahmood Rahman, Shiva Shankar Jena, Amir Shojakhani
# Jan 2022

# imports
import requests
import os
from pathlib import Path
import json
import pandas as pd
from dotenv import load_dotenv

import altair as alt
from textblob import TextBlob
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
nltk.download('stopwords')
from nltk.stem import SnowballStemmer
import string

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
        "expansions": "author_id,in_reply_to_user_id,geo.place_id",
        "tweet.fields": "id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source",
        "user.fields": "id,name,username,created_at,description,public_metrics,verified,entities",
        "place.fields": "full_name,id,country,country_code,geo,name,place_type",
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
        tweets_df.to_csv("output/tweets_response.csv", index=False)

    return tweets_df


def clean_tweets():
    """
    Cleans the text in the tweets.

    The cleaning process includes converting into lower case, removal of punctuation, hastags and hastag counts

    Parameters:
    -----------
    file_path : string
        file path in form of json or csv to fetch dataframe containing the tweets.

    Returns:
    --------
    df_tweets : dataframe
        A pandas dataframe comprising cleaned data in additional columns

    Examples
    --------
    >>> clean_tweets("tweets_df.json")
    """


def analytics(df, keyword):
    """Analysis the tweets of specific keyword in term of
    average number of retweets, the total number of
    comments, most used hashtags and the average number
    of likes of these tweets.

    Parameters
    ----------
    df : dataframe
        pandas dataframe
    keyword: str
        The keyword that the original dataframe extracted
        based on.

    Returns
    -------
    dict of str: int
        dict-like object where keys and values are
        related ratio or string including average number
        of retweets, the total number of comments, most
        used hashtags and the average number of likes

    Examples
    --------
    >>> from tweetlytics.tweetlytics import analytics
    >>> report = analytics(df,keyword)
    """


def plot_freq(df, col_text):
    """
    Takes in dataframe and analyzes 
        the hashtags to plot the most frequent ones.

    Parameters:
    -----------
    df : A pandas dataframe 
        consisting of the tweets

    text: string
        The column name of tweet text in dataframe.

    Returns:
    --------
    hash_plot: A bar chart
        A chart plotting analysis result of most frequent used hashtag words.
    """
    # Checking for valid inputs
    if not isinstance(df, pd.DataFrame):
        raise Exception("The argunment, df should take in a pandas dataframe")
    if type(col_text) != str:
        raise Exception("The argunment, col_text should take in a string")

    # get hashtags from text
    df['hash'] = df[col_text].apply(lambda x: re.findall(r'[#]\w+', x))

    # counting tags
    hash_dict = {}
    for hashtags in df["hash"]:
        for word in hashtags:
            hash_dict[word] = hash_dict.get(word, 0) + 1

    hash_df = pd.DataFrame(columns=['Keyword', 'Count'])
    for key, value in hash_dict.items():
        key_value = [[key, value]]
        hash_df = hash_df.append(pd.DataFrame(key_value, columns=['Keyword', 'Count']),
                                       ignore_index=True)

    # frequency plot
    hash_plot = alt.Chart(hash_df).mark_bar().encode(
        x=alt.X('Count', title="Hashtags"),
        y=alt.Y('Keyword', title="Count of Hashtags", sort='-x')
    ).properties(
        title='Top 15 Hashtag Words'
    ).transform_window(
        rank='rank(Count)',
        sort=[alt.SortField('Count', order='descending')]
    ).transform_filter((alt.datum.rank <= 15))

    return hash_plot