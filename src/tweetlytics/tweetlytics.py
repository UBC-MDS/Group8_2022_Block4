# Authors: Mahsa Sarafrazi, Mahmood Rahman, Shiva Shankar Jena, Amir Shojakhani
# Jan 2022

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
    