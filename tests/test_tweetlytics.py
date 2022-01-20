from tweetlytics import tweetlytics
from tweetlytics.tweetlytics import analytics
import numpy as np
import pandas as pd
from collections import Counter
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

def test_analytics():
    """Test the statestical information that are extracted from tweeter 
    on specific keyword."""
    
    
    analytics_df = analytics("tweets_response.csv", "Omicron")
    expected = 42
    actual = analytics("tweets_response.csv","Omicron").iloc[0,0] 
    assert actual == expected,  "number of likes is incorrect!"
    
    expected = 7
    actual = analytics("tweets_response.csv","Omicron").iloc[1,0]  
    assert actual == expected,  "number of comments is incorrect!"
    
    
    expected = 256578
    actual = analytics("tweets_response.csv","Omicron").iloc[2,0]  
    assert actual == expected,  "number of retweets is incorrect!"
    
    assert type(analytics_df) == pd.core.frame.DataFrame

    # Check the column names of the returned dataframe
    assert set(analytics_df.columns) == set(
        ["Keyword Analysis"]
    )
    
test_analytics()