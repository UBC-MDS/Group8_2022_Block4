import pandas as pd
from tweetlytics.tweetlytics import  tweet_senti_analys, senti_viz
from pytest import raises

def test_senti_viz():
    """
    Tests the senti_viz function to make sure the outputs are correct.
    Returns
    --------
    None
        The test should pass and no asserts should be displayed.
    """
    # Get test dataset
    data = pd.read_csv("tests/for_hash_plot.csv")
    
    # Run sentiment analysis
    sentiment = tweet_senti_analys(data)

    # Error Checks
    with raises(TypeError) as e:
        senti_viz(sentiment, "barchart")
    assert str(e.value) == "Invalid argument for plot_type: You must enter one of 'Standard', 'Stacked', 'Separate'"

    with raises(Exception) as e:
        senti_viz("data")
    assert str(e.value) == """The input of senti_tweet should be a Pandas DataFrame,
                           did you use output of tweet_senti_analys?"""

    with raises(KeyError) as e:
        senti_viz(data)
    assert str(e.value) == "'Input does not contain column for sentiment," \
                           " did you use output of tweet_senti_analys?'"

    # standard bar chart checks
    standard_plot = senti_viz(sentiment)
    assert str(type(standard_plot)) == "<class 'altair.vegalite.v4.api.Chart'>"
    assert standard_plot.encoding.x.shorthand == 'frequency', 'x_axis should be mapped to the x_axis'
    assert standard_plot.encoding.y.shorthand == 'Word', 'y_axis should be mapped to the y_axis'
    assert standard_plot.mark == 'bar'

    # concatenated bar chart check
    separate_plot = senti_viz(sentiment, "Separate")
    assert str(type(separate_plot)) == "<class 'altair.vegalite.v4.api.HConcatChart'>"
