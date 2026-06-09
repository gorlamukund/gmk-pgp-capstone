# app/agents/agent.py
# Agent that uses Anthropic SDK directly with tool calling

import anthropic
from loguru import logger

from app.core.config import settings
from app.services.retriever import RetrieverService

# Initialize retriever
retriever = RetrieverService()

# Initialize Anthropic client directly
client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)


class DocumentAgent:
    def __init__(self):
        self.model = settings.LLM_MODEL
        self.tools = [
            {
                "name": "search_documents",
                "description": "Search through SAP BTP documentation to find relevant information based on a query.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query to find relevant document chunks",
                        }
                    },
                    "required": ["query"],
                },
            }
        ]
        logger.info("DocumentAgent initialized successfully")

    def _search_documents(self, query: str) -> str:
        """Search ChromaDB for relevant chunks"""
        results = retriever.retrieve(query, top_k=3)
        if not results:
            return "No relevant information found in the documents."
        formatted = ""
        for i, chunk in enumerate(results):
            filename = chunk.metadata.get("filename", "Unknown")
            formatted += f"\n[Source {i + 1} - {filename}]:\n{chunk.text}\n"
        return formatted

    def query(self, user_question: str) -> dict:
        """Process user question using Anthropic tool calling"""
        logger.info(f"Agent processing: {user_question}")

        try:
            messages = [{"role": "user", "content": user_question}]
            system = """You are a helpful SAP BTP Document Assistant.
Always use the search_documents tool to find information before answering.
Base your answers only on the retrieved document content.
If you cannot find relevant information, say so clearly."""

            # Agentic loop
            while True:
                response = client.messages.create(
                    model=self.model,
                    max_tokens=settings.LLM_MAX_TOKENS,
                    system=system,
                    tools=self.tools,
                    messages=messages,
                )

                # If Claude wants to use a tool
                if response.stop_reason == "tool_use":
                    # Add Claude's response to messages
                    messages.append({"role": "assistant", "content": response.content})

                    # Process each tool call
                    tool_results = []
                    for block in response.content:
                        if block.type == "tool_use":
                            logger.info(
                                f"Agent using tool: {block.name} with query: {block.input}"
                            )
                            if block.name == "search_documents":
                                result = self._search_documents(block.input["query"])
                            else:
                                result = "Tool not found"

                            tool_results.append(
                                {
                                    "type": "tool_result",
                                    "tool_use_id": block.id,
                                    "content": result,
                                }
                            )

                    # Add tool results to messages
                    messages.append({"role": "user", "content": tool_results})

                # If Claude is done
                elif response.stop_reason == "end_turn":
                    final_answer = ""
                    for block in response.content:
                        if hasattr(block, "text"):
                            final_answer += block.text

                    logger.success("Agent answered successfully")
                    return {"answer": final_answer, "status": "success"}

        except Exception as e:
            logger.error(f"Agent error: {str(e)}")
            return {
                "answer": "I encountered an error while processing your question. Please try again.",
                "status": "error",
                "error": str(e),
            }
