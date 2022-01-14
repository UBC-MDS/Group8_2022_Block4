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