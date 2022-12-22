import configparser
import praw as praw


# Authorized instance
def get_reddit_instance(config_file):
    """
        This function returns an authorized instance of the reddit API.
        It takes a config file as an argument.
        The config file should be in the format:
        [REDDIT]
        client_id = <your client id>
        client_secret = <your client secret>
        user_agent = <your user agent>
        username = <your reddit_app username>
        password = <your reddit_app password>
    """

    config = configparser.ConfigParser()
    config.read(config_file)
    reddit_app = config['REDDIT']

    reddit = praw.Reddit(client_id=reddit_app['client_id'],  # your client id
                         client_secret=reddit_app['client_secret'],  # your client secret
                         user_agent=reddit_app['user_agent'],  # your user agent
                         username=reddit_app['username'],  # your reddit_app username
                         password=reddit_app['password'])  # your reddit_app password
    return reddit
