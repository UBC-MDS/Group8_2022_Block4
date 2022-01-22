# Authors: Mahsa Sarafrazi, Mahmood Rahman, Shiva Shankar Jena, Amir Shojakhani
# Jan 2022

# imports
import requests
import os
from pathlib import Path
import json
import pandas as pd
from dotenv import load_dotenv

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


def plot_tweets(df, time_def):
    """
    Plotting the number of tweets per hour, throughout 24 hours
    Plotting hashtags in tweets, and plot the hashtag analysis.
    Plotting user's tweets with sentimental analysis

    Parameters:
    -----------
    df : dataframe
        pandas dataframe
    time_def: string
        The column name of post time in dataframe.
    tweet: string
        The column name of tweet text in dataframe.
    sentiment_df : dataframe
        Output of tweet_sentiment_analysis,
        dataframe that contains added columns from tweet_sentiment_analysis
    plot_type : string
        Optional: Type of plot to return, 3 options:'Standard', 'Stacked', and 'Separate'
        'Standard' Returns bar plot of most common words tweeted color coded by sentiment
        'Stacked' Returns same as 'Standard' but if words are found in other sentiments they are stacked together
        'Separate' Returns 3 bar plots with the sentiment of 'Postive' 'Neutral', and 'Negative' separated
    Returns:
    --------
    plot: chart
        A histogram line plot plotting the counts of tweets versus hours.
        A chart plotting analysis result of most frequent used hashtag words.
        A bar plot of the user's tweets containing in order
        the most common words, colour coded by the word's sentiment class.

    Examples
    --------
    >>> from tweetlytics.tweetlytics import plot_tweets
    >>> plot = plot_tweets(df,time_def)
    """






































































































































































def senti_viz(senti_tweet, plot_type="Standard"):
    """
    Taking the output from senti_tweet,
    this function vizualizes plot

    Parameters:
    -----------
    senti_tweet : dataframe
        Output of tweet_sentiment_analysis,
        dataframe that contains added columns from tweet_sentiment_analysis

    plot_type : string
        Optional: Type of plot to return, 3 options:'Standard', 'Stacked', and 'Separate'
        'Standard' Returns bar plot of most common words tweeted color coded by sentiment
        'Stacked' Returns same as 'Standard' but if words are found in other sentiments they are stacked together
        'Separate' Returns 3 bar plots with the sentiment of 'Postive' 'Neutral', and 'Negative' separated

    Returns:
    --------
     plot:
        A bar plot of the user's tweets containing in order
        the most common words, colour coded by the word's sentiment class.
    """

    # check inputs
    options = ("Standard", "Stacked", "Separate")
    if plot_type not in options:
        raise TypeError("Invalid argument for plot_type: You must enter one of 'Standard', 'Stacked', 'Separate'")
    elif not isinstance(senti_tweet, pd.DataFrame):
        raise Exception("""The input of senti_tweet should be a Pandas DataFrame,
                           did you use output of tweet_sentiment_analysis?""")
    elif 'sentiment' not in senti_tweet:
        raise KeyError("Input does not contain column for sentiment, did you use output of tweet_sentiment_analysis?")

    # Define tweet_rank function
    def tweet_rank(df, sentiment):
        """function to return most common words tweeted for a specified sentiment"""
        df_senti = df[df['sentiment'] == sentiment]
        countVectorizer = CountVectorizer(analyzer=cleaning_text, stop_words='english')
        countVector = countVectorizer.fit_transform(df_senti['clean_tweets'])
        count_vect_df = pd.DataFrame(countVector.toarray(), columns=countVectorizer.get_feature_names())
        count_vect_df.head()
        count = pd.DataFrame(count_vect_df.sum())
        countdf = count.sort_values(0, ascending=False).head(20)
        return countdf[1:11]

    dataframes = dict()            # create empty dictionary to store sentiment dataframes
    for sentiment in np.unique(senti_tweet["sentiment"]):
        sent_df = tweet_rank(senti_tweet, sentiment)
        sent_df.columns = ['frequency']                # rename columns and include column for sentiment and word
        sent_df["sentiment"] = sentiment
        sent_df['Word'] = sent_df.index
        dataframes[sentiment] = sent_df     # append sentiment dataframe to dictionary

    # add all dataframes together, may need adjustment later
    top_words_df = pd.concat([dataframes['positive'], dataframes['neutral'], dataframes['negative']])

    # Plot if standard is selected
    if plot_type == "Standard":
        top_words_df['Word'] = top_words_df['Word'] + ' (' + top_words_df["sentiment"] + ')'
        standard_plot = alt.Chart(top_words_df, title='Most Common Words used by Twitter User').mark_bar().encode(
            x=alt.X('frequency', title='Number of Occurences'),
            y=alt.Y('Word', sort='-x'),
            color=alt.Color("sentiment", scale=alt.Scale(domain=['positive', 'neutral', 'negative'],
                            range=['blue', 'orange', 'red'])))
        return standard_plot

    # Plot if stacked is selected
    elif plot_type == "Stacked":
        top_words_df['Word'] = top_words_df.index
        stacked_plot = alt.Chart(top_words_df, title='Most Common Words used by Twitter User').mark_bar().encode(
            x=alt.X('frequency', title='Number of Occurences'),
            y=alt.Y('Word', sort='-x'),
            color=alt.Color("sentiment", scale=alt.Scale(domain=['positive', 'neutral', 'negative'],
                            range=['blue', 'orange', 'red'])))
        return stacked_plot

    # Plot if Separate is selected
    elif plot_type == "Separate":
        negative = alt.Chart(dataframes['negative'],
                             title='Most Common Negative Words used by Twitter User').mark_bar().encode(
            x=alt.X('frequency', title='Number of Occurences'),
            y=alt.Y('Word', sort='-x'),
            color=alt.value("red"))

        positive = alt.Chart(dataframes['positive'],
                             title='Most Common Postive Words used by Twitter User').mark_bar().encode(
            x=alt.X('frequency', title='Number of Occurences'),
            y=alt.Y('Word', sort='-x'),
            color=alt.value("blue"))

        neutral = alt.Chart(dataframes['neutral'],
                            title='Most Common Neutral Words used by Twitter User').mark_bar().encode(
            x=alt.X('frequency', title='Number of Occurences'),
            y=alt.Y('Word', sort='-x'),
            color=alt.value("orange"))

        separate_plot = positive | neutral | negative
        return separate_plot

