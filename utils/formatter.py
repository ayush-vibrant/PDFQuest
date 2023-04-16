import textwrap


def format_docs(docs):
    """
    Formats a list of documents and returns a well-formatted string.

    Args:
        docs (list): A list of documents where each document is a dictionary with keys 'page_content'
                     and 'metadata'.

    Returns:
        str: A well-formatted string.
    """
    output = ""
    for doc in docs:
        output += "=" * 50 + "\n"
        output += f"Source: {doc.metadata['source']}\n\n"
        output += textwrap.fill(doc.page_content, width=80) + "\n\n"
    return output
