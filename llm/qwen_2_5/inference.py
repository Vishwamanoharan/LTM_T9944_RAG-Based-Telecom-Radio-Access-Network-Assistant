
import gc
import torch

from llm.qwen_2_5.tokenizer_loader import QwenTokenizerLoader
from llm.qwen_2_5.model_loader import QwenModelLoader


class QwenInference:

    def __init__(self):

        self.tokenizer_loader = QwenTokenizerLoader()
        self.model_loader = QwenModelLoader()

        # Models are loaded only when generate() is called.
        self.tokenizer = None
        self.model = None

    def load(self):

        if self.tokenizer is None:
            self.tokenizer = self.tokenizer_loader.load()

        if self.model is None:
            self.model = self.model_loader.load_model()

        return self.model

    def generate(
        self,
        prompt,
        max_new_tokens=128,
        temperature=0.7
    ):

        if prompt is None or not str(prompt).strip():
            raise ValueError("Prompt cannot be empty.")

        # Lazy model initialization
        self.load()

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a Telecom RAN AI Assistant. "
                    "Answer questions about 4G, 5G, O-RAN, "
                    "RAN KPIs, network performance, and "
                    "3GPP specifications accurately. "
                    "Use the supplied evidence. "
                    "If evidence is insufficient, say so. "
                    "Do not invent technical facts."
                )
            },
            {
                "role": "user",
                "content": str(prompt).strip()
            }
        ]

        formatted_prompt = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        inputs = self.tokenizer(
            formatted_prompt,
            return_tensors="pt",
            truncation=True,
            max_length=1536
        )

        with torch.inference_mode():

            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                pad_token_id=self.tokenizer.eos_token_id
            )

        input_length = inputs["input_ids"].shape[1]

        generated_tokens = outputs[0][input_length:]

        response = self.tokenizer.decode(
            generated_tokens,
            skip_special_tokens=True
        )

        return response.strip()

    def close(self):

        if self.model is not None:
            del self.model
            self.model = None

        self.model_loader.model = None

        if self.tokenizer is not None:
            del self.tokenizer
            self.tokenizer = None

        self.tokenizer_loader.tokenizer = None

        gc.collect()

        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        print("Qwen model and tokenizer released.")
