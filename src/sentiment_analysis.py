from transformers import pipeline
import pandas as pd

def compute_bert_sentiment(df):
    classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    sentiments = classifier(df["review"].tolist(), truncation=True)
    df["sentiment_label"] = [s['label'] for s in sentiments]
    df["sentiment_score"] = [s['score'] for s in sentiments]
    return df
