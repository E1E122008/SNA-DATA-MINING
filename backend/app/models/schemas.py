from pydantic import BaseModel
from typing import List, Dict, Any

class NetworkResult(BaseModel):
    graph_json: Dict[str, Any]
    influencers: List[Dict[str, Any]]

class TextResult(BaseModel):
    tfidf: List[Dict[str, Any]]
    word_freq: List[Dict[str, Any]]
    wordcloud_img: str

class SentimentResult(BaseModel):
    sentiment_stats: Dict[str, float]
    user_sentiment: List[Dict[str, Any]]

class AnalysisResult(BaseModel):
    network: NetworkResult
    text: TextResult
    sentiment: SentimentResult 