# app/services/retriever.py
# Searches ChromaDB for relevant document chunks based on user query

import chromadb
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from loguru import logger

from app.core.config import settings


class RetrieverService:
    def __init__(self):
        # Connect to existing ChromaDB
        self.chroma_client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
        self.collection = self.chroma_client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION_NAME
        )

        # Same embedding model used during ingestion
        self.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

        # Set up vector store and index
        vector_store = ChromaVectorStore(chroma_collection=self.collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        self.index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store, embed_model=self.embed_model
        )

        logger.info("RetrieverService initialized successfully")

    def retrieve(self, query: str, top_k: int = 3) -> list:
        """Retrieve top_k most relevant chunks for a given query"""

        retriever = self.index.as_retriever(similarity_top_k=top_k)

        results = retriever.retrieve(query)

        logger.info(f"Retrieved {len(results)} chunks for query: {query}")

        return results
