import pandas as pd

# Group by bank, theme, sentiment_label, count occurrences
theme_counts = df.groupby(['bank', 'identified_theme', 'sentiment_label']).size().reset_index(name='count')

# Pivot to get positive and negative counts side-by-side
pivot = theme_counts.pivot_table(index=['bank', 'identified_theme'], columns='sentiment_label', values='count', fill_value=0).reset_index()

# Calculate difference or ratio to identify drivers/pain points
pivot['net_sentiment'] = pivot.get('positive', 0) - pivot.get('negative', 0)

# For each bank, find top drivers (high positive net_sentiment) and pain points (high negative net_sentiment)
drivers = pivot[pivot['net_sentiment'] > 0].sort_values(['bank', 'net_sentiment'], ascending=[True, False])
pain_points = pivot[pivot['net_sentiment'] < 0].sort_values(['bank', 'net_sentiment'])
