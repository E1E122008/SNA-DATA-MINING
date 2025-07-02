from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter

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
    return {'tfidf': tfidf_result, 'word_freq': word_freq_result} 