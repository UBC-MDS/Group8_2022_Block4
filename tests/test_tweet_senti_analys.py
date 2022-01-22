import pandas as pd
from tweetlytics.tweetlytics import tweet_senti_analys
from pytest import raises


def test_tweet_senti_analys():
    """
    Test existing functionalities of tweet_senti_analys(),
    which supposed to be a dataframe with sentiment results
    """
    
    # Calling helper function to create data
    data = pd.read_csv("tests/for_hash_plot.csv"))
    result = tweet_senti_analys(data)

    # make sure the input is a dataframe
    assert type(result) == pd.core.frame.DataFrame

    # make sure the output has the correct columns
    assert sum(result.columns == ['clean_tweets', 'polarity', 'subjectivity',
                                  'sentiment', 'neg', 'neu', 'pos', 'compound'])

    # make sure the output is not empty.
    assert len(result) > 0


def test_tweet_senti_analys_error():
    """
    Test error cases and error messages thrown by tweet_senti_analys.
    3 tests in total.
    """
    # test invalid input
    with raises(TypeError) as e:
        tweet_senti_analys('@ShawnMendes')
    assert str(e.value) == 'Invalid argument type: input must be a dataframe.'
