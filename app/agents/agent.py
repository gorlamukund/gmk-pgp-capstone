# app/agents/agent.py
# Agent using LlamaIndex ReActAgent with Anthropic LLM
# Implements guideline 8: Agent-based reasoning via ReActAgent

import asyncio
import concurrent.futures

from llama_index.core.agent import ReActAgent
from llama_index.llms.anthropic import Anthropic
from loguru import logger

from app.agents.tools import tools  # search_tool + summarize_tool from tools.py
from app.core.config import settings


def _run_async(coro):
    """Run a coroutine in a fresh thread with its own event loop.
    Avoids conflicts with uvloop or any existing loop Streamlit holds."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(asyncio.run, coro)
        return future.result()


SYSTEM_PROMPT = """You are a helpful SAP BTP Document Assistant.
Always use the search_documents tool to find information before answering.
Base your answers only on the retrieved document content.
If you cannot find relevant information, say so clearly."""


class DocumentAgent:
    def __init__(self):
        self.llm = Anthropic(
            model=settings.LLM_MODEL,
            max_tokens=settings.LLM_MAX_TOKENS,
            api_key=settings.ANTHROPIC_API_KEY,
            system_prompt=SYSTEM_PROMPT,
        )

        # ReActAgent — satisfies guideline 8 requirement
        self.agent = ReActAgent(
            tools=tools,
            llm=self.llm,
            verbose=True,
            timeout=60.0,
        )

        logger.info("DocumentAgent (ReActAgent) initialized successfully")

    def query(self, user_question: str) -> dict:
        """Process user question using LlamaIndex ReActAgent."""
        logger.info(f"Agent processing: {user_question}")

        try:

            async def _query():
                handler = self.agent.run(user_question)
                return await handler

            result = _run_async(_query())
            answer = str(result)

            logger.success("Agent answered successfully")
            return {"answer": answer, "status": "success"}

        except Exception as e:
            logger.error(f"Agent error: {str(e)}")
            import traceback

            logger.error(traceback.format_exc())
            return {
                "answer": "I encountered an error while processing your question. Please try again.",
                "status": "error",
                "error": str(e),
            }
