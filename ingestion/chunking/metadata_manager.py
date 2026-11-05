class MetadataManager:

    def create_metadata(
        self,
        source,
        document_name,
        chunk_id
    ):

        return {
            "source": source,
            "document": document_name,
            "chunk_id": chunk_id
        }