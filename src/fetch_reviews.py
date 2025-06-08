from google_play_scraper import reviews, Sort
import pandas as pd

def fetch_reviews(app_id: str, bank_name: str, max_reviews: int = 400) -> pd.DataFrame:
    all_reviews = []
    count = 0
    next_token = None

    while count < max_reviews:
        batch, next_token = reviews(
            app_id,
            lang='en',
            country='us',
            sort=Sort.NEWEST,
            count=200,
            continuation_token=next_token
        )
        all_reviews.extend(batch)
        count = len(all_reviews)
        if not next_token:
            break

    df = pd.DataFrame(all_reviews)[['content', 'score', 'at']]
    df.columns = ['review', 'rating', 'date']
    df['bank'] = bank_name
    df['source'] = 'Google Play'
    return df
