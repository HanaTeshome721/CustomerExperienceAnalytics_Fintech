import pandas as pd
from langdetect import detect

def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

def preprocess_reviews(df: pd.DataFrame) -> pd.DataFrame:
    # Remove duplicate and missing reviews
    df.drop_duplicates(subset=['review'], inplace=True)
    df.dropna(subset=['review', 'rating', 'date'], inplace=True)

    # Normalize dates
    df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.strftime('%Y-%m-%d')
    df.dropna(subset=['date'], inplace=True)

    # Detect and filter non-English reviews
    df['lang'] = df['review'].apply(detect_language)
    df = df[df['lang'] == 'en']
    df.drop(columns=['lang'], inplace=True)

    return df
