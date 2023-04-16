from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredPDFLoader


def load_document_pages(file_path):
    loader = UnstructuredPDFLoader(file_path)
    pages = loader.load()

    num_pages = len(pages)
    print(f'{num_pages} document(s) loaded from {file_path}')

    if num_pages > 0:
        num_chars = len(pages[0].page_content)
        print(f'The first page contains {num_chars} characters')

    return pages


def split_document_into_chunks(pages):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=20,
        length_function=len)
    texts = text_splitter.split_documents(pages)

    num_texts = len(texts)
    print(f'The documents have been split into {num_texts} chunks')

    return texts
