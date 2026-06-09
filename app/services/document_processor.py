# app/services/document_processor.py
# Handles reading and extracting text from different document formats

import json
import os

import pandas as pd
import PyPDF2
import yaml
from loguru import logger


class DocumentProcessor:
    SUPPORTED_FORMATS = [
        ".pdf",
        ".txt",
        ".csv",
        ".xlsx",
        ".json",
        ".yaml",
        ".yml",
        ".md",
    ]

    def process(self, file_path: str) -> str:
        """Main method - detects file type and extracts text"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        extension = os.path.splitext(file_path)[1].lower()

        if extension not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported format: {extension}")

        logger.info(f"Processing file: {file_path}")

        if extension == ".pdf":
            return self._process_pdf(file_path)
        elif extension == ".txt":
            return self._process_txt(file_path)
        elif extension == ".md":
            return self._process_markdown(file_path)
        elif extension == ".csv":
            return self._process_csv(file_path)
        elif extension == ".xlsx":
            return self._process_excel(file_path)
        elif extension == ".json":
            return self._process_json(file_path)
        elif extension in [".yaml", ".yml"]:
            return self._process_yaml(file_path)

    def _process_pdf(self, file_path: str) -> str:
        """Extract text from PDF files"""
        text = ""
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text

    def _process_txt(self, file_path: str) -> str:
        """Extract text from TXT files"""
        with open(file_path, encoding="utf-8") as f:
            return f.read()

    def _process_markdown(self, file_path: str) -> str:
        """Extract text from Markdown files"""
        with open(file_path, encoding="utf-8") as f:
            return f.read()

    def _process_csv(self, file_path: str) -> str:
        """Extract text from CSV files"""
        df = pd.read_csv(file_path)
        return df.to_string()

    def _process_excel(self, file_path: str) -> str:
        """Extract text from Excel files"""
        df = pd.read_excel(file_path)
        return df.to_string()

    def _process_json(self, file_path: str) -> str:
        """Extract text from JSON files"""
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
        return json.dumps(data, indent=2)

    def _process_yaml(self, file_path: str) -> str:
        """Extract text from YAML files"""
        with open(file_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return yaml.dump(data)
