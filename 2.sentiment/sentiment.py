from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import pika
import sys
import os
import json

nltk.download('vader_lexicon')

tweet = "Hej. It is a good day today! I am very happy."


def analyze_sentiment(text):
    score = SentimentIntensityAnalyzer().polarity_scores(text)
    pos = score['pos']
    neu = score['neu']
    neg = score['neg']
    # comp = score['compound']
    return (pos, neu, neg)

# TEST
# print(analyze_sentiment( "Hej. It is a good day today! I am very happy."))


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='ingest')


def callback(ch, method, properties, body):
    print(" [x] Received new tweet! %s" % body)
    status = json.loads(body)
    (pos, neu, neg) = analyze_sentiment(status["text"])

    status["sentiment"] = {'pos': pos, 'neu': neu, 'neg': neg}
    channel.basic_publish(
        exchange='', routing_key='persistence', body=json.dumps(status))


channel.basic_consume(
    queue='ingest', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
