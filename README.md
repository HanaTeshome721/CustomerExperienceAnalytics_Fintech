## Methodology

1. Collected 400+ Google Play reviews each from 3 banking apps using `google-play-scraper`.
2. Fetched fields: review content, rating, date, app name.
3. Applied preprocessing:
   - Removed duplicates.
   - Handled missing data.
   - Normalized date format to YYYY-MM-DD.
4. Combined and saved as a single clean CSV file in `/data`.
