class QueryProcessor:

    def clean(self, query):

        if query is None:
            return ""

        query = str(query).strip()

        query = " ".join(
            query.split()
        )

        return query

    def process(self, query):

        cleaned_query = self.clean(query)

        return {
            "original_query": query,
            "processed_query": cleaned_query,
            "valid": bool(cleaned_query)
        }

    def is_valid(self, query):

        return bool(
            self.clean(query)
        )