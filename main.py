# main.py
# SAP BTP Document Assistant - Entry point

import sys

from loguru import logger

from app.core.config import settings

# Configure loguru to output to terminal
logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <level>{message}</level>",
)


def main():
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"LLM Model: {settings.LLM_MODEL}")
    logger.info(f"ChromaDB Path: {settings.CHROMA_DB_PATH}")
    logger.info(f"Debug Mode: {settings.DEBUG}")

    # Verify API key is loaded
    if not settings.ANTHROPIC_API_KEY:
        logger.error("ANTHROPIC_API_KEY is missing from .env file!")
        return

    logger.success("Configuration loaded successfully!")
    logger.success(f"{settings.APP_NAME} is ready!")


if __name__ == "__main__":
    main()
