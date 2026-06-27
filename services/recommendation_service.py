import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RecommendationService:

    def __init__(self, df):

        self.df = df.copy()

        # Create TF-IDF Vectorizer
        self.vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        # Convert descriptions into vectors
        self.tfidf_matrix = self.vectorizer.fit_transform(
            self.df["description"]
        )

    # -------------------------------------------------

    def recommend(self, query, top_n=10):

        # Convert user query into vector
        query_vector = self.vectorizer.transform([query])

        # Calculate similarity
        similarity = cosine_similarity(
            query_vector,
            self.tfidf_matrix
        ).flatten()

        # Store similarity
        recommendations = self.df.copy()

        recommendations["similarity"] = (
            similarity * 100
        ).round(2)

        # Sort by similarity
        recommendations = recommendations.sort_values(
            by="similarity",
            ascending=False
        )

        return recommendations.head(top_n)

    # -------------------------------------------------

    def recommend_similar(self, laptop_name, top_n=5):

        laptop = self.df[
            self.df["name"].str.lower() ==
            laptop_name.lower()
        ]

        if laptop.empty:
            return pd.DataFrame()

        index = laptop.index[0]

        similarity = cosine_similarity(
            self.tfidf_matrix[index],
            self.tfidf_matrix
        ).flatten()

        recommendations = self.df.copy()

        recommendations["similarity"] = (
            similarity * 100
        ).round(2)

        recommendations = recommendations.sort_values(
            by="similarity",
            ascending=False
        )

        # Remove the selected laptop itself
        recommendations = recommendations[
            recommendations["name"] != laptop_name
        ]

        return recommendations.head(top_n)