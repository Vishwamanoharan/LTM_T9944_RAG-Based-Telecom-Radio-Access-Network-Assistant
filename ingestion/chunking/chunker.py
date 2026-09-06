from .chunk_config import CHUNK_SIZE, CHUNK_OVERLAP


class TextChunker:

    def __init__(self):

        self.chunk_size = CHUNK_SIZE
        self.chunk_overlap = CHUNK_OVERLAP

    def chunk_text(self, text):

        chunks = []

        if not text:
            return chunks

        start = 0

        while start < len(text):

            end = start + self.chunk_size

            chunk = text[start:end]

            if chunk.strip():

                chunks.append(
                    chunk.strip()
                )

            start += (
                self.chunk_size
                - self.chunk_overlap
            )

        return chunks

    def chunk_records(self, records):

        chunks = []

        chunk_id = 1

        for record in records:

            question = record.get(
                "question",
                ""
            )

            answer = record.get(
                "answer",
                ""
            )

            source = record.get(
                "source",
                "Unknown"
            )

            text = (
                f"Question: {question}\n"
                f"Answer: {answer}"
            )

            text_chunks = self.chunk_text(text)

            for chunk in text_chunks:

                chunks.append({
                    "chunk_id": chunk_id,
                    "source": source,
                    "text": chunk
                })

                chunk_id += 1

        return chunks

    def chunk_pdf_pages(
        self,
        pages,
        source,
        document
    ):

        chunks = []

        chunk_id = 1

        for page_data in pages:

            page_number = page_data["page"]

            text = page_data["text"]

            text_chunks = self.chunk_text(text)

            for chunk in text_chunks:

                chunks.append({
                    "chunk_id": chunk_id,
                    "source": source,
                    "document": document,
                    "page": page_number,
                    "text": chunk
                })

                chunk_id += 1

        return chunks