# streamlit_app.py
# Streamlit UI for SAP BTP Document Assistant

import os

import streamlit as st
from loguru import logger

from app.agents.agent import DocumentAgent
from app.core.config import settings
from app.services.document_processor import DocumentProcessor
from app.services.ingestion import IngestionService
from app.utils.guardrails import GuardrailsService
from app.utils.validator import InputValidator

# Page configuration
st.set_page_config(
    page_title="SAP BTP Document Assistant", page_icon="🤖", layout="wide"
)

# Initialize services in session state
if "agent" not in st.session_state:
    with st.spinner("Initializing Document Assistant..."):
        st.session_state.agent = DocumentAgent()
        st.session_state.processor = DocumentProcessor()
        st.session_state.ingestion = IngestionService()
        st.session_state.validator = InputValidator()
        st.session_state.guardrails = GuardrailsService()
        st.session_state.chat_history = []
        st.session_state.uploaded_files = []

# Title
st.title("🤖 SAP BTP Document Assistant")
st.caption(f"Powered by Claude AI | Version {settings.APP_VERSION}")

# Sidebar - Document Upload
with st.sidebar:
    st.header("📁 Document Upload")
    st.caption("Upload documents to query against")

    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "txt", "csv", "xlsx", "json", "yaml", "md"],
        help="Supported formats: PDF, TXT, CSV, Excel, JSON, YAML, Markdown. Max size: 10MB",
    )

    if uploaded_file is not None:
        if uploaded_file.name not in st.session_state.uploaded_files:
            with st.spinner(f"Processing {uploaded_file.name}..."):
                try:
                    # Save uploaded file temporarily
                    temp_path = f"data/temp_{uploaded_file.name}"
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    # Validate file before processing
                    validation = st.session_state.validator.validate_file(
                        temp_path, uploaded_file.name
                    )

                    if not validation.is_valid:
                        st.error(f"❌ {validation.error_message}")
                        os.remove(temp_path)
                    else:
                        # Process and ingest
                        text = st.session_state.processor.process(temp_path)
                        chunks = st.session_state.ingestion.ingest(
                            text, uploaded_file.name
                        )

                        # Clean up temp file
                        os.remove(temp_path)

                        st.session_state.uploaded_files.append(uploaded_file.name)
                        st.success(f"✅ {uploaded_file.name} ingested successfully!")
                        logger.info(f"File uploaded and ingested: {uploaded_file.name}")

                except Exception as e:
                    st.error(f"❌ Error processing file: {str(e)}")
                    logger.error(f"Upload error: {str(e)}")
                    if os.path.exists(temp_path):
                        os.remove(temp_path)

    # Show uploaded files
    if st.session_state.uploaded_files:
        st.divider()
        st.subheader("📚 Ingested Documents")
        for fname in st.session_state.uploaded_files:
            st.markdown(f"✅ {fname}")

    st.divider()
    st.caption("SAP BTP documentation is pre-loaded and ready to query.")

    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

# Main chat interface
st.subheader("💬 Ask a Question")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask anything about SAP BTP..."):
    # Validate query first
    query_validation = st.session_state.validator.validate_query(prompt)

    if not query_validation.is_valid:
        st.warning(f"⚠️ {query_validation.error_message}")
    else:
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Add to history
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                result = st.session_state.agent.query(prompt)

            raw_answer = result.get("answer", "")

            # Apply guardrails
            validated = st.session_state.guardrails.validate_response(
                raw_answer, prompt
            )
            formatted_answer = st.session_state.guardrails.format_response(validated)

            st.markdown(formatted_answer)

            # Add to history
            st.session_state.chat_history.append(
                {"role": "assistant", "content": formatted_answer}
            )
