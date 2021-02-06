import tweepy
import sys
import os
from dotenv import load_dotenv
import csv
import re
import pika
import datetime
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='ingest')


# Load credentials from .env file
load_dotenv()

"""https://stackoverflow.com/a/49986645/3711660"""


def deEmojify(text):
    regrex_pattern = re.compile(pattern="["
                                u"\U0001F600-\U0001F64F"  # emoticons
                                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                "]+", flags=re.UNICODE)
    return regrex_pattern.sub(r'', text)


# 1. Authenticate
auth = tweepy.OAuthHandler(os.getenv('CONSUMER_KEY'),
                           os.getenv('CONSUMER_SECRET'))
auth.set_access_token(os.getenv('ACCESS_TOKEN'),
                      os.getenv('ACCESS_TOKEN_SECRET'))
api = tweepy.API(auth)

if (not api):
    print("Authentication failed!")
    sys.exit(-1)


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, track: str):
        self.track = track

    def on_status(self, status):
        obj = {'text': deEmojify(status.text),
               'author': status.user.screen_name,
               'author_id': status.user.id,
               'time': status.created_at.isoformat(),
               'track': self.track}
        print(dir(status))
        channel.basic_publish(
            exchange='', routing_key='ingest', body=json.dumps(obj))

    def on_error(self, status_code):
        print(status_code)


print('twitter ingestion in progress...')
track = "news"

myStreamListener = MyStreamListener(track)
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
myStream.filter(track=[track], languages=['en'])


connection.close()
