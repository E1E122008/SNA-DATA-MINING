from fastapi import APIRouter, UploadFile, File, Form
from app.services import preprocessing, network_analysis, text_analysis, sentiment
from app.models.schemas import AnalysisResult
import pandas as pd
from collections import Counter

router = APIRouter()

@router.post("/analyze")
async def analyze_instagram_data(
    file: UploadFile = File(...),
    columns: str = Form(...),  # comma-separated
    analysis_type: str = Form(...),  # e.g. "tag", "like"
    keywords: str = Form(None)  # comma-separated
):
    df = preprocessing.handle_upload(file, columns)
    network_result = network_analysis.analyze(df, analysis_type)
    text_result = text_analysis.analyze(df, keywords)
    sentiment_result = sentiment.analyze(df)

    # Statistik tambahan
    total_likes = int(df['likes'].sum()) if 'likes' in df.columns else None
    avg_caption_length = float(df['caption'].apply(lambda x: len(str(x).split())).mean()) if 'caption' in df.columns else None
    unique_hashtag_count = 0
    if 'caption' in df.columns:
        hashtags = []
        for cap in df['caption']:
            hashtags += [w for w in str(cap).split() if w.startswith('#')]
        unique_hashtag_count = len(set(hashtags))
    # Top user by jumlah post
    top_user_post = []
    if 'username' in df.columns:
        top_user_post = Counter(df['username']).most_common(5)
    # Top user by rata-rata likes
    top_user_likes = []
    if 'username' in df.columns and 'likes' in df.columns:
        avg_likes_per_user = df.groupby('username')['likes'].mean().sort_values(ascending=False).head(5)
        top_user_likes = [(user, float(likes)) for user, likes in avg_likes_per_user.items()]
    # Top mentioned user
    top_mentioned_user = []
    if 'tagged_users' in df.columns:
        all_tagged = []
        for tags in df['tagged_users']:
            all_tagged += tags if isinstance(tags, list) else []
        top_mentioned_user = Counter(all_tagged).most_common(5)
    # Most active day
    most_active_day = None
    if 'tanggal_posting' in df.columns:
        most_active = Counter(df['tanggal_posting']).most_common(1)
        if most_active:
            most_active_day = most_active[0][0]

    # Mapping ke struktur frontend
    data_mining = {
        'total_user': df['username'].nunique() if 'username' in df.columns else None,
        'total_post': len(df),
        'total_likes': total_likes,
        'avg_likes': float(df['likes'].mean()) if 'likes' in df.columns else None,
        'avg_caption_length': avg_caption_length,
        'unique_hashtag_count': unique_hashtag_count,
        'top_hashtag': [w['word'] for w in text_result['word_freq'] if w['word'].startswith('#')][:5] if 'word_freq' in text_result and text_result['word_freq'] else [],
        'top_user_post': top_user_post,
        'top_user_likes': top_user_likes,
        'top_mentioned_user': top_mentioned_user,
        'most_active_day': most_active_day
    }
    # Top hashtag dari word_freq jika ada
    if 'word_freq' in text_result and text_result['word_freq']:
        data_mining['top_hashtag'] = [w['word'] for w in text_result['word_freq'] if w['word'].startswith('#')][:5]

    # TF-IDF: top_words berisi list of dict {word, score}
    tfidf = {
        'top_words': text_result['tfidf'][:10] if 'tfidf' in text_result else []
    }

    sentiment_stats = sentiment_result.get('sentiment_stats', {})
    # Ambil top user untuk setiap kategori dari seluruh data
    all_sentiments = sentiment_result.get('all_sentiments', [])
    top_positive_users = [s['user'] for s in sorted(all_sentiments, key=lambda x: -x['score']) if s['sentiment'] == 'positive'][:5]
    top_neutral_users  = [s['user'] for s in sorted(all_sentiments, key=lambda x: -abs(x['score'])) if s['sentiment'] == 'neutral'][:5]
    top_negative_users = [s['user'] for s in sorted(all_sentiments, key=lambda x: x['score']) if s['sentiment'] == 'negative'][:5]

    sentiment_data = {
        'positif': round(sentiment_stats.get('positive', 0) * 100),
        'netral': round(sentiment_stats.get('neutral', 0) * 100),
        'negatif': round(sentiment_stats.get('negative', 0) * 100),
        'top_positive_users': top_positive_users,
        'top_neutral_users': top_neutral_users,
        'top_negative_users': top_negative_users
    }

    network = {
        'graph_url': network_result.get('graph_url'),
        'influencer': [i['user'] for i in network_result.get('influencers', [])[:5]],
        'influencer_details': network_result.get('influencers', [])[:10]
    }

    return {
        'data_mining': data_mining,
        'tfidf': tfidf,
        'sentiment': sentiment_data,
        'network': network
    } 