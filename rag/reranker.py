from sentence_transformers import CrossEncoder


class Reranker:

    def __init__(
        self,
        model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"
    ):
        print("Loading reranker model...")

        self.model = CrossEncoder(model_name)

        print("Reranker model loaded successfully.")

    def rerank(self, query, results, top_k=3):
        """
        Rerank retrieved chunks using a Cross-Encoder.
        """

        if not results:
            return []

        pairs = [
            [query, result["chunk"]["text"]]
            for result in results
        ]

        scores = self.model.predict(pairs)

        reranked = []

        for result, score in zip(results, scores):

            item = result.copy()

            item["reranker_score"] = float(score)

            reranked.append(item)

        reranked.sort(
            key=lambda x: x["reranker_score"],
            reverse=True
        )

        return reranked[:top_k]
