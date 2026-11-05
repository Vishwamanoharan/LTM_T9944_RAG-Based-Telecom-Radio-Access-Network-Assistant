from pathlib import Path


class OptimizationPrompt:

    def __init__(self):
        self.template_path = (
            Path(__file__).resolve().parents[2]
            / "rag_engine"
            / "prompt_templates"
            / "optimization_prompt.txt"
        )

    def load_template(self):
        if not self.template_path.exists():
            raise FileNotFoundError(
                f"Prompt template not found: "
                f"{self.template_path}"
            )

        return self.template_path.read_text(
            encoding="utf-8"
        )

    def build(
        self,
        query,
        context
    ):
        if query is None:
            raise ValueError(
                "Query cannot be None."
            )

        if context is None:
            context = ""

        query = str(query).strip()
        context = str(context).strip()

        if not query:
            raise ValueError(
                "Query cannot be empty."
            )

        template = self.load_template()

        return template.format(
            query=query,
            context=context
        )