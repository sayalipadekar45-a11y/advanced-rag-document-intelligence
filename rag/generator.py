class AnswerGenerator:

    def __init__(self):

        print(
            "Local answer generator loaded."
        )

        # Minimum reranker score required
        # before generating an answer.
        self.min_relevance_score = -1.0

    def generate_answer(
        self,
        question,
        retrieved_chunks
    ):

        if not retrieved_chunks:

            return {
                "answer":
                "The uploaded documents do not contain enough information to answer this question.",

                "sources": []
            }

        # Best retrieved result
        best_result = retrieved_chunks[0]

        best_chunk = best_result["chunk"]

        best_score = best_result.get(
            "reranker_score",
            -999
        )

        # Hallucination protection
        if best_score < self.min_relevance_score:

            return {
                "answer":
                "The uploaded documents do not contain enough relevant information to answer this question.",

                "sources": []
            }

        source = best_chunk.get(
            "source",
            "Unknown document"
        )

        page = best_chunk.get(
            "page",
            "Unknown"
        )

        answer = (
            "Based on the uploaded documents:\n\n"
            f"Source: {source}\n"
            f"Page: {page}\n\n"
            f"{best_chunk['text']}"
        )

        sources = []

        for result in retrieved_chunks:

            chunk = result["chunk"]

            sources.append({

                "document":
                chunk.get(
                    "source",
                    "Unknown document"
                ),

                "page":
                chunk.get(
                    "page",
                    "Unknown"
                ),

                "chunk_id":
                chunk.get(
                    "chunk_id",
                    "Unknown"
                ),

                "score":
                result.get(
                    "reranker_score",
                    result.get(
                        "hybrid_score",
                        0
                    )
                )
            })

        return {

            "answer":
            answer,

            "sources":
            sources
        }