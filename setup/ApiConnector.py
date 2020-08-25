import praw
import traceback
import requests
import json


class ApiConnector:
    #def __init__(self):

    def redditConnector(self, use_script, client_secret, user_agent, username, password):
        try:
            redditObject = praw.Reddit(client_id=use_script,
                                 client_secret=client_secret,
                                 user_agent=user_agent,
                                 username=username,
                                 password=password)

            print(f"Connection to Reddit established.")
            return redditObject

        except Exception as e:
            print(f"Could not connect to Reddit. Error: {e}")
