class MetadataManager:

    def create_metadata(
        self,
        source,
        document_name,
        chunk_id,
        page=None
    ):

        metadata = {
            "source": source,
            "document": document_name,
            "chunk_id": chunk_id
        }

        if page is not None:
            metadata["page"] = page

        return metadata