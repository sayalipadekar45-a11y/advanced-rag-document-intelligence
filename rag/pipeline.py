from rag.document_loader import extract_text
from rag.chunker import create_chunks
from rag.embeddings import EmbeddingModel
from rag.vector_store import FAISSVectorStore
from rag.bm25_retriever import BM25Retriever
from rag.hybrid_retriever import HybridRetriever
from rag.reranker import Reranker
from rag.generator import AnswerGenerator


class RAGPipeline:

    def __init__(self, file_paths):

        print("\nInitializing RAG Pipeline...\n")

        if isinstance(file_paths, str):
            file_paths = [file_paths]

        all_chunks = []

        for file_path in file_paths:

            print(f"Processing: {file_path}")

            pages = extract_text(file_path)

            chunks = create_chunks(pages)

            for chunk in chunks:

                chunk["source"] = file_path

            all_chunks.extend(chunks)

        self.chunks = all_chunks

        print(
            "Total chunks created:",
            len(self.chunks)
        )

        self.embedding_model = EmbeddingModel()

        texts = [
            chunk["text"]
            for chunk in self.chunks
        ]

        embeddings = self.embedding_model.encode(
            texts
        )

        self.vector_store = FAISSVectorStore(
            embeddings.shape[1]
        )

        self.vector_store.add_documents(
            embeddings,
            self.chunks
        )

        self.bm25 = BM25Retriever(
            self.chunks
        )

        self.hybrid = HybridRetriever(
            self.vector_store,
            self.bm25
        )

        self.reranker = Reranker()

        self.generator = AnswerGenerator()

        # Conversation history
        self.chat_history = []

        print(
            "\nRAG Pipeline initialized successfully.\n"
        )

    def ask(self, question, top_k=5):

        # Build contextual query
        contextual_query = question

        if self.chat_history:

            previous_turns = self.chat_history[-3:]

            history_text = "\n".join(
                [
                    f"User: {turn['question']}\n"
                    f"Assistant: {turn['answer']}"
                    for turn in previous_turns
                ]
            )

            contextual_query = (
                "Previous conversation:\n"
                + history_text
                + "\n\nCurrent question:\n"
                + question
            )

        # Query embedding
        query_embedding = self.embedding_model.encode(
            [contextual_query]
        )

        # Hybrid retrieval
        candidates = self.hybrid.search(
            query_embedding,
            question,
            top_k=top_k
        )

        # Re-ranking
        reranked = self.reranker.rerank(
            question,
            candidates,
            top_k=3
        )

        # Generate answer
        response = self.generator.generate_answer(
            question,
            reranked
        )

        # Save conversation
        self.chat_history.append({
            "question": question,
            "answer": response["answer"]
        })

        return {
            "question": question,
            "answer": response["answer"],
            "sources": response["sources"],
            "retrieved_chunks": reranked,
            "chat_history_length": len(
                self.chat_history
            )
        }