import os

import streamlit as st

from QASystem import QASystem
from openai_utils import init_embeddings_object
from chroma_vector_store import ChromaSearch
from pdf_utils import load_document_pages, split_document_into_chunks
from pinecone_vector_store import PineconeSearch
from formatter import format_docs
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="PDF QA Tool", page_icon=":magic_wand:", layout="centered")

st.title(" :magic_wand: OlxPert: PDF Question-Answering Tool")
st.caption("OlxPert is an AI-powered PDF QA tool that enables you to easily upload and analyze PDF documents"
           " with advanced question-answering capabilities. "
           " OlxPert goes beyond traditional keyword-based search "
           " and utilizes vector embeddings and semantic search "
           "to deliver precise and efficient results"
           " from your PDFs to improve your workflow efficiency.")
st.divider()


def run_app():
    uploader = PDFUploader()

    # Load PDF file
    uploader.load_pdf()

    # Upload the documents to cloud/local session
    uploader.upload()

    if "run_qa" not in st.session_state:
        st.session_state.run_qa = False

    if not st.session_state.run_qa:
        if st.button("Run Question-Answering Task"):
            st.session_state.run_qa = True
    else:
        uploader.run_qa()
        if uploader.show_qa:
            uploader.display_result()
        if st.button("Clear", key="qa_clear_button"):
            st.session_state.run_qa = False


class PDFUploader:
    def __init__(self):
        self.file_path = None
        self.pages = None
        self.texts = None
        self.file_key = "test"
        self.question = None
        self.result = None
        self.vector_store = None
        self.embeddings = None
        self.use_pinecone = os.environ.get('USE_PINECONE', 'false').lower() == 'true'
        self.run_qa_with_source = os.environ.get('QA_WITH_SOURCE', 'false').lower() == 'true'
        self.show_qa = False

    def load_pdf(self):
        self.file_path = st.file_uploader("Upload PDF", type="pdf")
        if self.file_path:
            if self.file_path.type == "application/pdf":
                print("PDF uploaded successfully.")
                st.write("PDF uploaded successfully.")
                self.pages = load_document_pages(self.file_path)
                self.texts = split_document_into_chunks(self.pages)
            else:
                st.error("Please upload a PDF file.")

    def upload(self):
        if self.texts:
            self.embeddings = init_embeddings_object()
            search_strategy = self.get_search_strategy()
            self.vector_store = search_strategy.push_documents(self.texts, self.embeddings)
            st.write("PDF text uploaded to vector store.")

    def get_search_strategy(self):
        if self.use_pinecone:
            print("Using Pinecone search strategy")
            search_strategy = PineconeSearch()
        else:
            print("Using Chroma search strategy")
            search_strategy = ChromaSearch()
        return search_strategy

    def run_qa(self):
        if self.vector_store:
            qa_system = QASystem()
            self.question = st.text_input("Enter your question:", key='textbox', placeholder="Enter your question here")
            if st.button("Ask"):
                print(f"use source? {self.run_qa_with_source}")
                if self.run_qa_with_source:
                    self.result = qa_system.retrieve_document(self.vector_store, self.question)
                else:
                    self.result = qa_system.qa_without_sources(self.vector_store, self.question)
                self.show_qa = True
        else:
            st.warning("Please upload a PDF file and click on Ask button.")

    @staticmethod
    def clear_callback():
        st.session_state['textbox'] = ''

    def display_result(self):
        if self.result:
            st.write(f"Question: {self.question}")
            st.write(f"Answer: {self.result['result']}")
            if self.run_qa_with_source:
                with st.expander("Show Source"):
                    st.write("The relevant source documents are:")
                    source = format_docs(self.result['source_documents'])
                    st.write(f"Source: {source}")
            if st.button("Clear", on_click=self.clear_callback):
                self.question = None
                self.result = None
                self.show_qa = False
        else:
            st.warning("Please run the question-answering task first.")


if __name__ == '__main__':
    run_app()
