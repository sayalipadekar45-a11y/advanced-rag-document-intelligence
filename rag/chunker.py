import re


def clean_text(text):
    """
    Clean extra spaces and line breaks.
    """

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def create_chunks(
    pages,
    chunk_size=100,
    overlap=20
):
    """
    Create word-based chunks.

    chunk_size = number of words in each chunk
    overlap = number of words shared between chunks
    """

    chunks = []

    global_chunk_id = 0

    for page_data in pages:

        page_number = page_data["page"]

        text = clean_text(
            page_data["text"]
        )

        if not text:
            continue

        words = text.split()

        start = 0

        while start < len(words):

            end = start + chunk_size

            chunk_words = words[start:end]

            chunk_text = " ".join(
                chunk_words
            )

            if chunk_text.strip():

                chunks.append({

                    "chunk_id":
                    global_chunk_id,

                    "page":
                    page_number,

                    "text":
                    chunk_text.strip()

                })

                global_chunk_id += 1

            if end >= len(words):
                break

            start = end - overlap

    return chunks