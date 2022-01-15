# Authors: Mahsa Sarafrazi, Mahmood Rahman, Shiva Shankar Jena, Amir Shojakhani
# Jan 2022

def get_store():
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
    store_path: string
        The string path to store the retrieved tweets in
        Json format.
    store_csv: boolean
        Create .csv file with response data or not.
        Default is False.
    return_pandas_df: boolean
        return pandas data frame or not.
        Is required for further text analysis in this package.
        Default is True.
    include_public_metrics : boolean
        Should public metrics regarding each tweet such as
        impression_count, like_count, reply_count, retweet_count,
        url_link_clicks and user_profile_clicks be downloaded
        and stored. Default is True.
    Returns:
    --------
    tweets_df : dataframe
        A pandas dataframe of retrieved tweets based on user's
        selected parameters. (Data will be stored as a Json file)
    """
    return

def clean_tweets():
    """
    Cleans the text in the tweets.
    
    The cleaning process includes converting into lower case, removal of punctuation and counting the hastags in the tweets
    
    Parameters:
    -----------
    file_path : string
        file path in form of json or csv to fetch dataframe containing the tweets.
    
    Returns:
    --------
    df_tweets : dataframe
        A pandas dataframe comprising cleaned tweets and hashtag counts per tweet
    
    Examples
    --------
    >>> clean_tweets("tweets_df.json")
    """
  
def analytics(df,keyword):
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

def plot_histo(df, time_def):
    """
    Plotting the number of tweets per hour, throughout 24 hours
    Parameters:
    -----------
    df : dataframe
        pandas dataframe
    time_def: string
        The column name of post time in dataframe.
    Returns:
    --------
    histo_plot: chart
        A histogram line plot plotting the counts of tweets versus hours.
        
    Examples
    --------
    >>> from tweetlytics.tweetlytics import plot_histo
    >>> histo_plot = plot_histo(df,time_def)
    """