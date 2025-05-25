import ast
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class ServiceSearch:
    """
    A class to handle searching for services based on user queries.
    It uses a pre-trained SentenceTransformer model to compute embeddings
    and find the most similar services.
    """

    def __init__(self, question: str):
        """
        Initializes the ServiceSearch with a query string.
        :param question: str, the search question
        """

        self.query = question
        self.model = SentenceTransformer("cointegrated/LaBSE-en-ru")
        self.df = pd.read_csv("data/processed/services_with_embeddings.csv")

    def detect_category(self) -> pd.DataFrame:
        """
        Detects the category of the service based on the query.
        Filters the DataFrame based on keywords related to service categories.
        :return: DataFrame containing services that match the query category
        :raises ValueError: If no services match the query category
        """

        keywords_map = {
            "зарплатный проект": ["зарплат", "salary"],
            "карта": ["карт"],
            "кредит": ["кредит", "займ"],
            "депозит": ["депозит", "вклад"],
            "перевод": ["перевод"],
        }

        lower_query = self.query.lower()
        matched_category = None
        for category, keywords in keywords_map.items():
            if any(kw in lower_query for kw in keywords):
                matched_category = category
                break
        if matched_category:
            filtered_df = self.df[self.df["service_name"] == matched_category]
            self.df = filtered_df
        if self.df.empty:
            raise ValueError("Нет услуг, соответствующих вашему запросу.")
        return self.df

    def get_results(self, top_k=1) -> pd.DataFrame:
        """
        Searches for services similar to the query.
        :param top_k: int, number of top results to return
        :return: DataFrame containing the top_k most similar services
        """

        self.df["embedding"] = self.df["embedding"].apply(ast.literal_eval)
        self.detect_category()

        query_embedding = self.model.encode(self.query)
        description_embeddings = np.vstack(self.df["embedding"].values)

        similarities = cosine_similarity([query_embedding], description_embeddings)[0]
        top_indices = similarities.argsort()[::-1][:top_k]
        return self.df.iloc[top_indices]

    def search(self) -> dict:
        """
        Formats the search results into a user-friendly string.
        :return: str, formatted response with service details
        """
        response = {"text": "", "url": ""}
        results = self.get_results(1)
        if results.empty:
            response["text"] = "Извините, я не нашёл подходящих услуг по вашему запросу."
            return response
        response["text"] = "Вот что я нашёл:\n"
        response["text"] += f"\n🔹 {results['full_text'].values[0][:1000]}"
        response["url"] = results["url"].values[0]
        return response
