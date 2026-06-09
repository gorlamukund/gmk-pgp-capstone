# app/agents/tools.py
# Defines tools available to the ReActAgent

from llama_index.core.tools import FunctionTool
from loguru import logger

from app.services.retriever import RetrieverService

# Initialize retriever
retriever = RetrieverService()


def search_documents(query: str) -> str:
    """
    Search through SAP BTP documentation and return relevant content.
    Use this tool when you need to find information from the uploaded documents.

    Args:
        query: The search query to find relevant document chunks

    Returns:
        Relevant document content as a string
    """
    logger.info(f"Agent searching documents for: {query}")

    results = retriever.retrieve(query, top_k=3)

    if not results:
        return "No relevant information found in the documents."

    # Format results for agent consumption
    formatted = ""
    for i, chunk in enumerate(results):
        filename = chunk.metadata.get("filename", "Unknown")
        formatted += f"\n[Source {i + 1} - {filename}]:\n{chunk.text}\n"

    return formatted


def summarize_topic(topic: str) -> str:
    """
    Search and summarize information about a specific topic from SAP BTP documentation.
    Use this when the user wants a summary or overview of a topic.

    Args:
        topic: The topic to summarize

    Returns:
        A summary of relevant content about the topic
    """
    logger.info(f"Agent summarizing topic: {topic}")

    results = retriever.retrieve(topic, top_k=5)

    if not results:
        return "No information found about this topic in the documents."

    # Combine all chunks
    combined = "\n".join([chunk.text for chunk in results])

    return f"Here is the relevant content about '{topic}':\n\n{combined}"


# Create LlamaIndex FunctionTools
search_tool = FunctionTool.from_defaults(
    fn=search_documents,
    name="search_documents",
    description="Search through SAP BTP documentation to find relevant information based on a query.",
)

summarize_tool = FunctionTool.from_defaults(
    fn=summarize_topic,
    name="summarize_topic",
    description="Search and retrieve content about a specific topic from SAP BTP documentation.",
)

# List of all available tools
tools = [search_tool, summarize_tool]
