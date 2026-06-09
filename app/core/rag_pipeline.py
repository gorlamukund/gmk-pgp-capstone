# app/core/rag_pipeline.py
# Combines retrieved chunks with Claude to generate grounded answers

from llama_index.llms.anthropic import Anthropic
from loguru import logger

from app.core.config import settings
from app.services.retriever import RetrieverService


class RAGPipeline:
    def __init__(self):
        # Initialize Claude as the LLM
        self.llm = Anthropic(
            model=settings.LLM_MODEL,
            api_key=settings.ANTHROPIC_API_KEY,
            max_tokens=settings.LLM_MAX_TOKENS,
            temperature=settings.LLM_TEMPERATURE,
        )

        # Initialize retriever
        self.retriever = RetrieverService()

        logger.info("RAG Pipeline initialized successfully")

    def query(self, user_question: str) -> dict:
        """
        Main method - takes user question and returns grounded answer
        1. Retrieves relevant chunks from ChromaDB
        2. Builds prompt with retrieved context
        3. Sends to Claude for answer generation
        """

        logger.info(f"Processing query: {user_question}")

        # Step 1: Retrieve relevant chunks
        retrieved_chunks = self.retriever.retrieve(user_question)

        if not retrieved_chunks:
            return {
                "answer": "I could not find any relevant information in the uploaded documents.",
                "sources": [],
                "chunks_used": 0,
            }

        # Step 2: Build context from retrieved chunks
        context = "\n\n".join(
            [
                f"[Chunk {i + 1}]:\n{chunk.text}"
                for i, chunk in enumerate(retrieved_chunks)
            ]t
        )

        # Step 3: Build prompt
        prompt = f"""You are a helpful document assistant for SAP BTP Document Assistant.
Answer the user's question based ONLY on the provided document context below.
If the answer is not in the context, say "I don't have enough information in the uploaded documents to answer this."

Document Context:
{context}

User Question: {user_question}

Answer:"""

        # Step 4: Send to Claude
        response = self.llm.complete(prompt)

        # Step 5: Extract source filenames
        sources = list(
            set(
                [
                    chunk.metadata.get("filename", "Unknown")
                    for chunk in retrieved_chunks
                ]
            )
        )

        logger.success(
            f"Query answered successfully using {len(retrieved_chunks)} chunks"
        )

        return {
            "answer": response.text,
            "sources": sources,
            "chunks_used": len(retrieved_chunks),
        }
