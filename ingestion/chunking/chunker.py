from .chunk_config import CHUNK_SIZE
from .chunk_config import CHUNK_OVERLAP


class TextChunker:

    # =====================================================
    # GENERIC TEXT CHUNKING
    # =====================================================

    def chunk(self, text):

        if text is None:
            return []

        text = str(text)

        if not text.strip():
            return []

        step = CHUNK_SIZE - CHUNK_OVERLAP

        if step <= 0:
            raise ValueError(
                "CHUNK_OVERLAP must be smaller than CHUNK_SIZE"
            )

        chunks = []

        start = 0

        while start < len(text):

            end = start + CHUNK_SIZE

            chunk = text[start:end]

            if chunk.strip():
                chunks.append(chunk)

            start += step

        return chunks

    # =====================================================
    # JSON RECORD CHUNKING
    # =====================================================

    def chunk_records(self, records):

        if records is None:
            return []

        # If parser returns a single dictionary
        if isinstance(records, dict):

            # Handle common wrapper structures
            if "records" in records:
                records = records["records"]

            elif "data" in records:
                records = records["data"]

            else:
                records = [records]

        chunks = []

        if isinstance(records, list):

            for record in records:

                if isinstance(record, dict):

                    parts = []

                    for key, value in record.items():

                        if value is None:
                            continue

                        if isinstance(value, list):

                            value = " | ".join(
                                str(item)
                                for item in value
                            )

                        parts.append(
                            f"{key}: {value}"
                        )

                    text = "\n".join(parts)

                else:

                    text = str(record)

                record_chunks = self.chunk(text)

                chunks.extend(record_chunks)

        else:

            chunks.extend(
                self.chunk(str(records))
            )

        return chunks

    # =====================================================
    # PDF PAGE CHUNKING
    # =====================================================

    def chunk_pdf_pages(
        self,
        pages,
        source_type="3GPP",
        document_name=""
    ):

        if pages is None:
            return []

        chunks = []

        for page_number, page in enumerate(
            pages,
            start=1
        ):

            if isinstance(page, dict):

                if "text" in page:
                    text = page["text"]

                elif "content" in page:
                    text = page["content"]

                else:
                    text = " ".join(
                        str(value)
                        for value in page.values()
                        if value is not None
                    )

            else:

                text = str(page)

            page_chunks = self.chunk(text)

            for chunk_text in page_chunks:

                enriched_chunk = (
                    f"Source: {source_type}\n"
                    f"Document: {document_name}\n"
                    f"Page: {page_number}\n\n"
                    f"{chunk_text}"
                )

                chunks.append(enriched_chunk)

        return chunks