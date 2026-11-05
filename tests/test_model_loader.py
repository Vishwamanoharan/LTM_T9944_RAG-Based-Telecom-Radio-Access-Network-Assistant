from llm.qwen_2_5.model_loader import (
    QwenModelLoader
)


def main():

    print("\n================================")
    print("QWEN MODEL TEST")
    print("================================")

    loader = QwenModelLoader()

    model = loader.load_model()

    print("\nModel Type:")
    print(type(model))

    print("\nModel test passed.")


if __name__ == "__main__":
    main()