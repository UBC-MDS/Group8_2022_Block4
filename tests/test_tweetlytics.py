# Authors: Mahsa Sarafrazi, Mahmood Rahman, Shiva Shankar Jena, Amir Shojakhani
# Jan 2022

# imports
from tweetlytics.tweetlytics import clean_tweets
import pandas as pd
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()  # load .env files in the project folder
  
def test_clean_tweets():
    """
    Test various steps in clean_tweets function
    -Check for valid input parameters
    -check for outputs:
        -check if file_path exists
        -check if ouput dataframe is a pandas dataframe
        -check if output dataframe contains the desired columns
        -check if clean tweets column has any of the special 
        characters
    """
    file_path = "tests/output/tweets_response.csv"
        
    # Checking for outputs: storing cleaned data
    df = clean_tweets(file_path)
    
    # Checking for 'df' to be a dataframe
    if not isinstance(df, pd.DataFrame):
        raise Exception("'df' must be of DataFrame type.")
    
    # Checking for 'df' to be non-null dataframe
    if df.empty:
        raise Exception("'df' must not be empty or none type") 
    
    # Checking if 'text' column exists in dataframe
    if "text" not in df.columns.to_list():
        raise Exception("'text' column not present in dataframe" )
    
    
    # check if input parameter file path exists 
    assert os.path.exists("tests/output/tweets_response.csv")
    
    # check if output dataframe is a pandas dataframe
    assert type(df) == pd.core.frame.DataFrame
    
    # check if output dataframe contains the columns for cleaned data
    new_cols = ["clean_tokens", "clean_tweets", "word_count"]
    col_list = df.columns.to_list()
    "clean_tokens" in col_list
    assert all(elem in col_list for elem in new_cols)
    
    # check if clean_tweets column contains any alphanumeric character
    tweet =  []
    for i in range(len(df)):
        tweet.append(df.loc[i,"clean_tweets"])
    any(not c.isalnum() for c in tweet)
    
    
    
    
    