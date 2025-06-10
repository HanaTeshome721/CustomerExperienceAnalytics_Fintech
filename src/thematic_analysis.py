from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

def extract_keywords(df, top_n=20):
    tfidf = TfidfVectorizer(ngram_range=(1,2), stop_words='english', max_features=1000)
    tfidf_matrix = tfidf.fit_transform(df['review'])
    feature_names = tfidf.get_feature_names_out()
    scores = tfidf_matrix.sum(axis=0).A1
    keywords = pd.DataFrame({'keyword': feature_names, 'score': scores})
    return keywords.sort_values(by='score', ascending=False).head(top_n)
