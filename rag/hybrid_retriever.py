class HybridRetriever:

    def __init__(self, vector_store, bm25_retriever):
        self.vector_store = vector_store
        self.bm25_retriever = bm25_retriever

    def search(self, query_embedding, query, top_k=5):
        """
        Combine FAISS semantic retrieval and BM25 keyword retrieval.
        """

        # FAISS results
        faiss_results = self.vector_store.search(
            query_embedding,
            top_k=top_k
        )

        # BM25 results
        bm25_results = self.bm25_retriever.search(
            query,
            top_k=top_k
        )

        combined = {}

        # Add FAISS results
        for result in faiss_results:

            chunk_id = result["chunk"]["chunk_id"]

            combined[chunk_id] = {
                "chunk": result["chunk"],
                "faiss_score": result["score"],
                "bm25_score": 0.0
            }

        # Add BM25 results
        for result in bm25_results:

            chunk_id = result["chunk"]["chunk_id"]

            if chunk_id not in combined:
                combined[chunk_id] = {
                    "chunk": result["chunk"],
                    "faiss_score": 0.0,
                    "bm25_score": result["score"]
                }
            else:
                combined[chunk_id]["bm25_score"] = result["score"]

        # Normalize scores
        faiss_scores = [
            item["faiss_score"]
            for item in combined.values()
        ]

        bm25_scores = [
            item["bm25_score"]
            for item in combined.values()
        ]

        max_faiss = max(faiss_scores) if faiss_scores else 1
        max_bm25 = max(bm25_scores) if bm25_scores else 1

        # Calculate hybrid score
        for item in combined.values():

            normalized_faiss = (
                item["faiss_score"] / max_faiss
                if max_faiss > 0
                else 0
            )

            normalized_bm25 = (
                item["bm25_score"] / max_bm25
                if max_bm25 > 0
                else 0
            )

            item["hybrid_score"] = (
                0.6 * normalized_faiss
                + 0.4 * normalized_bm25
            )

        # Sort by hybrid score
        results = sorted(
            combined.values(),
            key=lambda x: x["hybrid_score"],
            reverse=True
        )

        return results[:top_k]
