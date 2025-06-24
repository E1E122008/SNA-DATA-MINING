from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze(df):
    df.columns = [c.lower() for c in df.columns]
    analyzer = SentimentIntensityAnalyzer()
    sentiments = []
    for idx, row in df.iterrows():
        text = str(row['caption'])
        score = analyzer.polarity_scores(text)
        if score['compound'] >= 0.05:
            label = 'positive'
        elif score['compound'] <= -0.05:
            label = 'negative'
        else:
            label = 'neutral'
        user = row['username']
        tagged = row.get('tagged_users', [])
        sentiments.append({'user': user, 'caption': text, 'sentiment': label, 'score': score['compound']})
    total = len(sentiments)
    pos = sum(1 for s in sentiments if s['sentiment'] == 'positive')
    neg = sum(1 for s in sentiments if s['sentiment'] == 'negative')
    neu = total - pos - neg
    sentiment_stats = {
        'positive': pos / total if total else 0,
        'negative': neg / total if total else 0,
        'neutral': neu / total if total else 0
    }
    user_sentiment = sorted(sentiments, key=lambda x: x['score'], reverse=True)[:10]
    return {'sentiment_stats': sentiment_stats, 'user_sentiment': user_sentiment} 