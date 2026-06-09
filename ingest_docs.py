# ingest_docs.py
# Ingests all documents from data/ folder into ChromaDB

import os
import sys

from loguru import logger

from app.services.document_processor import DocumentProcessor
from app.services.ingestion import IngestionService

# Configure logger
logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <level>{message}</level>",
)


def ingest_all_documents(data_folder: str = "data/"):
    """Walks through data/ folder and ingests all supported documents"""

    processor = DocumentProcessor()
    ingestion = IngestionService()

    # Track results
    success_count = 0
    error_count = 0
    skipped_count = 0
    total_chunks = 0

    logger.info(f"Starting ingestion from folder: {data_folder}")

    # Walk through all files recursively
    for root, dirs, files in os.walk(data_folder):
        for filename in files:
            file_path = os.path.join(root, filename)
            extension = os.path.splitext(filename)[1].lower()

            # Skip unsupported files
            if extension not in processor.SUPPORTED_FORMATS:
                skipped_count += 1
                continue

            try:
                # Extract text
                text = processor.process(file_path)

                # Skip empty files
                if not text.strip():
                    logger.warning(f"Empty file skipped: {filename}")
                    skipped_count += 1
                    continue

                # Ingest into ChromaDB
                total_chunks = ingestion.ingest(text, filename)
                success_count += 1
                logger.success(f"Ingested: {filename}")

            except Exception as e:
                logger.error(f"Error processing {filename}: {str(e)}")
                error_count += 1
                continue

    # Final summary
    logger.info("=" * 50)
    logger.success("Ingestion Complete!")
    logger.info(f"Successfully ingested : {success_count} files")
    logger.info(f"Skipped              : {skipped_count} files")
    logger.info(f"Errors               : {error_count} files")
    logger.info(f"Total chunks in DB   : {total_chunks}")


if __name__ == "__main__":
    ingest_all_documents()
