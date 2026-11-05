from transformers import (
    AutoModelForCausalLM
)

import torch


class QwenModelLoader:

    def __init__(
        self,
        model_name="Qwen/Qwen2.5-0.5B-Instruct"
    ):

        self.model_name = model_name

        self.model = None

    def load_model(self):

        if self.model is not None:
            return self.model

        print("\nLoading Qwen model...")
        print(f"Model: {self.model_name}")

        self.model = (
            AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float32,
                device_map=None
            )
        )

        self.model.eval()

        print(
            "Qwen model loaded successfully."
        )

        return self.model