from transformers import AutoTokenizer


class QwenTokenizerLoader:

    def __init__(
        self,
        model_name="Qwen/Qwen2.5-0.5B-Instruct"
    ):

        self.model_name = model_name

        self.tokenizer = None

    def load(self):

        if self.tokenizer is not None:

            return self.tokenizer

        print("\nLoading tokenizer...")
        print(
            f"Model: {self.model_name}"
        )

        self.tokenizer = (
            AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )
        )

        print(
            "Tokenizer loaded successfully."
        )

        return self.tokenizer