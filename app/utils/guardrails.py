# app/utils/guardrails.py
# Output safety checks and hallucination reduction

from loguru import logger

# Phrases that indicate the agent couldn't find an answer
NO_ANSWER_PHRASES = [
    "i don't have enough information",
    "i cannot find",
    "not found in the documents",
    "no relevant information",
    "i don't know",
    "unable to find",
    "not mentioned in",
    "no information available",
]

# Minimum acceptable response length
MIN_RESPONSE_LENGTH = 20


class GuardrailsService:
    def validate_response(self, response: str, query: str) -> dict:
        """
        Validates agent response before displaying to user.
        Returns a dictionary with validated answer and status.
        """

        # Check response is not empty
        if not response or not response.strip():
            logger.warning("Empty response received from agent")
            return {
                "answer": "I was unable to generate a response. Please try again.",
                "is_grounded": False,
                "warning": "Empty response",
            }

        response = response.strip()

        # Check response is not too short
        if len(response) < MIN_RESPONSE_LENGTH:
            logger.warning(f"Response too short: {response}")
            return {
                "answer": "I could not find enough information to answer your question. Please try rephrasing.",
                "is_grounded": False,
                "warning": "Response too short",
            }

        # Check if agent indicated it couldn't find an answer
        response_lower = response.lower()
        for phrase in NO_ANSWER_PHRASES:
            if phrase in response_lower:
                logger.info(f"Agent indicated no answer found for: {query}")
                return {
                    "answer": response,
                    "is_grounded": False,
                    "warning": "Agent could not find relevant information",
                }

        # Response passed all checks
        logger.info("Response passed guardrails checks")
        return {"answer": response, "is_grounded": True, "warning": None}

    def format_response(self, validated_response: dict) -> str:
        """
        Formats the validated response for display in Streamlit.
        Adds a warning if response is not grounded.
        """
        answer = validated_response["answer"]
        is_grounded = validated_response["is_grounded"]
        warning = validated_response["warning"]

        if not is_grounded and warning:
            formatted = f"{answer}\n\n---\n⚠️ *Note: This response may not be fully grounded in the uploaded documents.*"
        else:
            formatted = answer

        return formatted
