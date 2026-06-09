# app/utils/validator.py
# Input validation for file uploads and user queries

import os

from loguru import logger

# Constants
MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
MIN_QUERY_LENGTH = 3
MAX_QUERY_LENGTH = 500

# Suspicious patterns that might indicate prompt injection
SUSPICIOUS_PATTERNS = [
    "ignore previous instructions",
    "ignore all instructions",
    "disregard your instructions",
    "you are now",
    "forget everything",
    "new instructions",
    "system prompt",
]


class ValidationResult:
    """Holds the result of a validation check"""

    def __init__(self, is_valid: bool, error_message: str = ""):
        self.is_valid = is_valid
        self.error_message = error_message


class InputValidator:
    def validate_file(self, file_path: str, file_name: str) -> ValidationResult:
        """Validates an uploaded file before processing"""

        # Check file exists
        if not os.path.exists(file_path):
            logger.warning(f"File not found: {file_name}")
            return ValidationResult(False, "File not found.")

        # Check file size
        file_size = os.path.getsize(file_path)
        if file_size > MAX_FILE_SIZE_BYTES:
            logger.warning(f"File too large: {file_name} ({file_size} bytes)")
            return ValidationResult(
                False,
                f"File size exceeds {MAX_FILE_SIZE_MB}MB limit. Please upload a smaller file.",
            )

        # Check file is not empty
        if file_size == 0:
            logger.warning(f"Empty file: {file_name}")
            return ValidationResult(False, "File is empty. Please upload a valid file.")

        logger.info(f"File validation passed: {file_name}")
        return ValidationResult(True)

    def validate_query(self, query: str) -> ValidationResult:
        """Validates user query before sending to agent"""

        # Check query is not empty
        if not query or not query.strip():
            return ValidationResult(False, "Please enter a question.")

        query = query.strip()

        # Check minimum length
        if len(query) < MIN_QUERY_LENGTH:
            return ValidationResult(
                False,
                f"Question is too short. Please enter at least {MIN_QUERY_LENGTH} characters.",
            )

        # Check maximum length
        if len(query) > MAX_QUERY_LENGTH:
            return ValidationResult(
                False,
                f"Question is too long. Please keep it under {MAX_QUERY_LENGTH} characters.",
            )

        # Check for prompt injection attempts
        query_lower = query.lower()
        for pattern in SUSPICIOUS_PATTERNS:
            if pattern in query_lower:
                logger.warning(f"Suspicious query detected: {query}")
                return ValidationResult(
                    False,
                    "Your question contains invalid content. Please rephrase and try again.",
                )

        logger.info(f"Query validation passed: {query}")
        return ValidationResult(True)
