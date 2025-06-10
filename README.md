## Methodology

1. Collected 400+ Google Play reviews each from 3 banking apps using `google-play-scraper`.
2. Fetched fields: review content, rating, date, app name.
3. Applied preprocessing:
   - Removed duplicates.
   - Handled missing data.
   - Normalized date format to YYYY-MM-DD.
4. Combined and saved as a single clean CSV file in `/data`.
 Ethics & Biases
Note that online reviews tend to skew negative since people are more motivated to report issues.

Sentiment models can misclassify sarcasm or mixed feelings.

The sample may not represent all users equally (e.g., older customers might be underrepresented).