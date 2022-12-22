import config
import pandas as pd
import re


def get_subreddit_submissions(config_file, subreddit_name, sort_filter='top', time_filter='all', limit=100):
    """
        Get submissions from a subreddit.

        Parameters
        ----------
        config_file : str
            The path to the configuration file.
        subreddit_name : str
            The name of the subreddit to get submissions from.
        sort_filter : str, optional
            The type of submissions to get.
            Valid values are: 'top', 'hot', 'rising', 'new'
            Default is 'top'.
        time_filter : str, optional
            The time period to get submissions from.
            Valid values are: 'all', 'day', 'hour', 'month', 'week', 'year'
            Default is 'all'.
        limit : int, optional
            The maximum number of submissions to get.
            Maximum possible is 1000.
            Default is 100.

        Returns
        -------
        df : pandas.DataFrame
            A dataframe containing the submissions.
            Columns: submission_id, comment_id, original_text, processed_text
    """

    # Authorized instance
    reddit = config.get_reddit_instance(config_file)
    # Get subreddit
    subreddit = reddit.subreddit(subreddit_name)
    # Get submissions by sort_filter type
    if sort_filter.lower() == 'top':
        submissions = subreddit.top(time_filter=time_filter, limit=limit)
    elif sort_filter.lower() == 'hot':
        submissions = subreddit.hot(limit=limit)
    elif sort_filter.lower() == 'rising':
        submissions = subreddit.rising(limit=limit)
    else:
        submissions = subreddit.new(limit=limit)

    # Save submission to dataframe df
    # Create df
    df = pd.DataFrame(columns=['submission_id', 'comment_id', 'original_text', 'processed_text'])
    for submission in submissions:
        # Process submission text, removing any non-alphanumeric or space characters using ASCII-only matching
        processed = re.sub("[^\w\s]", '', submission.selftext, flags=re.ASCII).lower()
        # Creates a new row as a series and adds it to the end of the dataframe
        new_row = pd.Series(
            {'submission_id': submission.id, 'original_text': submission.selftext, 'processed_text': processed})
        df = pd.concat([df, new_row.to_frame().T], ignore_index=True)

    return df