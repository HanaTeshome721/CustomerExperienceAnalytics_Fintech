import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load your data
df = pd.read_csv("../data/sentiment_reviews.csv")

# 2. (Optional) Data cleaning/preprocessing here if needed

# 3. Calculate average sentiment and rating per bank
avg_sentiment = df.groupby('bank')['sentiment_score'].mean()
avg_rating = df.groupby('bank')['rating'].mean()

print("Average sentiment scores:\n", avg_sentiment)
print("Average ratings:\n", avg_rating)

# 4. Continue with drivers, pain points, visualizations, etc.
