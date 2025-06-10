import sys
import os
import pandas as pd

# Add src to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Task 1 imports
from fetch_reviews import fetch_reviews
from preprocess import preprocess_reviews

# Task 2 imports
from sentiment_analysis import compute_bert_sentiment
from thematic_analysis import extract_keywords


def run_task_1():
    apps = {
        'com.combanketh.mobilebanking': 'CBE',
        'com.boa.boaMobileBanking': 'BOA',
        'com.dashen.dashensuperapp': 'Dashen'
    }

    dfs = []

    for app_id, bank_name in apps.items():
        print(f" Fetching reviews for {bank_name}...")
        df = fetch_reviews(app_id, bank_name)
        df = preprocess_reviews(df)
        dfs.append(df)

    final_df = pd.concat(dfs, ignore_index=True)

    os.makedirs("data", exist_ok=True)
    final_df.to_csv("data/cleaned_reviews.csv", index=False)
    print("✅ Saved cleaned reviews to 'data/cleaned_reviews.csv'")


def run_task_2():
    print("📊 Running Sentiment and Thematic Analysis...")
    df = pd.read_csv("data/cleaned_reviews.csv")
    df = compute_bert_sentiment(df)
    df.to_csv("data/sentiment_reviews.csv", index=False)
    print("✅ Saved sentiment-annotated reviews to 'data/sentiment_reviews.csv'")

    for bank in df["bank"].unique():
        bank_df = df[df["bank"] == bank]
        keywords = extract_keywords(bank_df)
        keywords.to_csv(f"data/{bank}_keywords.csv", index=False)
        print(f"📝 Saved keywords for {bank} to 'data/{bank}_keywords.csv'")


def main():
    if len(sys.argv) < 2:
        print("❗Usage: python main.py [task-1 | task-2]")
        sys.exit(1)

    task = sys.argv[1]

    if task == "task-1":
        run_task_1()
    elif task == "task-2":
        run_task_2()
    else:
        print(f"❗Unknown task: {task}")
        sys.exit(1)


if __name__ == "__main__":
    main()
