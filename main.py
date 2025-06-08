import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from fetch_reviews import fetch_reviews
from preprocess import preprocess_reviews
import pandas as pd

def main():
    apps = {
         'com.combanketh.mobilebanking': 'CBE',
         'com.boa.boaMobileBanking': 'BOA',
         'com.dashen.dashensuperapp': 'Dashen'
    }

    dfs = []

    for app_id, bank_name in apps.items():
        print(f"Fetching reviews for {bank_name}...")
        df = fetch_reviews(app_id, bank_name)
        df = preprocess_reviews(df)
        dfs.append(df)

    final_df = pd.concat(dfs, ignore_index=True)

    os.makedirs("data", exist_ok=True)
    final_df.to_csv("data/cleaned_reviews.csv", index=False)
    print("✅ Saved cleaned reviews to 'data/cleaned_reviews.csv'.")

if __name__ == "__main__":
    main()
