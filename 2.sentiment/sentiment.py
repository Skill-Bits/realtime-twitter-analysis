from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')

tweet = "Hej. It is a good day today! I am very happy."
def analyze_sentiment(text):
    score = SentimentIntensityAnalyzer().polarity_scores(tweet)
    pos = score['pos']
    neu = score['neu']
    neg = score['neg']
    # comp = score['compound']
    return (pos, neu, neg)

print(analyze_sentiment(tweet))

