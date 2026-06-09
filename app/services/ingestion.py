# app/services/ingestion.py
# Chunks text and stores embeddings in ChromaDB

import chromadb
from llama_index.core import Document, StorageContext, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from loguru import logger

from app.core.config import settings


class IngestionService:
    def __init__(self):
        # Initialize ChromaDB
        self.chroma_client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
        self.collection = self.chroma_client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION_NAME
        )

        # Initialize embedding model
        self.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

        # Initialize text splitter
        self.splitter = SentenceSplitter(
            chunk_size=settings.CHUNK_SIZE, chunk_overlap=settings.CHUNK_OVERLAP
        )

        logger.info("IngestionService initialized successfully")

    def ingest(self, text: str, filename: str) -> int:
        """Takes extracted text, chunks it and stores in ChromaDB"""

        # Create a LlamaIndex Document
        document = Document(text=text, metadata={"filename": filename})

        # Set up ChromaDB vector store
        vector_store = ChromaVectorStore(chroma_collection=self.collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        # Create index — this chunks, embeds and stores automatically
        index = VectorStoreIndex.from_documents(
            documents=[document],
            storage_context=storage_context,
            embed_model=self.embed_model,
            transformations=[self.splitter],
        )

        logger.info(f"Successfully ingested: {filename}")

        # Return number of chunks created
        return self.collection.count()
