from rank_bm25 import BM25Okapi


class BM25Retriever:

    def __init__(self, chunks):
        self.chunks = chunks

        tokenized_documents = [
            chunk["text"].lower().split()
            for chunk in chunks
        ]

        self.bm25 = BM25Okapi(tokenized_documents)

    def search(self, query, top_k=5):
        """
        Search chunks using BM25 keyword matching.
        """

        tokenized_query = query.lower().split()

        scores = self.bm25.get_scores(tokenized_query)

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )[:top_k]

        results = []

        for index in ranked_indices:

            results.append({
                "score": float(scores[index]),
                "chunk": self.chunks[index]
            })

        return results