from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
from wordcloud import WordCloud
import base64
from io import BytesIO

def analyze(df, keywords):
    df.columns = [c.lower() for c in df.columns]
    captions = df['caption'].astype(str).tolist()
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(captions)
    tfidf_scores = zip(vectorizer.get_feature_names_out(), tfidf_matrix.sum(axis=0).tolist()[0])
    tfidf_sorted = sorted(tfidf_scores, key=lambda x: x[1], reverse=True)[:20]
    tfidf_result = [{'word': w, 'score': s} for w, s in tfidf_sorted]
    all_words = ' '.join(captions).split()
    word_freq = Counter(all_words).most_common(20)
    word_freq_result = [{'word': w, 'count': c} for w, c in word_freq]
    wc = WordCloud(width=400, height=200, background_color='white').generate(' '.join(captions))
    img = BytesIO()
    wc.to_image().save(img, format='PNG')
    wordcloud_img = base64.b64encode(img.getvalue()).decode()
    return {'tfidf': tfidf_result, 'word_freq': word_freq_result, 'wordcloud_img': wordcloud_img} 