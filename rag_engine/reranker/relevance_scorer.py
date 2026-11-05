import torch

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)


class RelevanceScorer:

    def __init__(
        self,
        model_name="farbodtavakkoli/OTel-Reranker-0.6B"
    ):

        print("\nLoading telecom reranker model...")
        print(f"Model: {model_name}")

        self.model_name = model_name

        self.tokenizer = (
            AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )
        )

        self.model = (
            AutoModelForSequenceClassification.from_pretrained(
                self.model_name,
                trust_remote_code=True,
                torch_dtype=torch.float32
            )
        )

        self.model.eval()

        print(
            "Telecom reranker model loaded successfully."
        )

    def score(self, query, documents):

        if query is None:
            raise ValueError(
                "Query cannot be None."
            )

        query = str(query).strip()

        if not query:
            raise ValueError(
                "Query cannot be empty."
            )

        if not documents:
            return []

        texts = []

        for document in documents:

            text = document.get(
                "text",
                ""
            )

            text = str(text).strip()

            texts.append(text)

        scores = []

        for text in texts:

            inputs = self.tokenizer(
                query,
                text,
                return_tensors="pt",
                truncation=True,
                max_length=512,
                padding=True
            )

            with torch.no_grad():

                outputs = self.model(
                    **inputs
                )

            logits = outputs.logits

            if logits.ndim == 2:

                score = logits[0, -1]

            else:

                score = logits[0]

            scores.append(
                float(score.item())
            )

        return scores