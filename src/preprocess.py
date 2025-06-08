import pandas as pd

def preprocess_reviews(df: pd.DataFrame) -> pd.DataFrame:
    df.drop_duplicates(subset=['review'], inplace=True)
    df.dropna(subset=['review', 'rating', 'date'], inplace=True)
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    return df
