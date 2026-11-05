from llm.qwen_2_5.tokenizer_loader import (
    QwenTokenizerLoader
)


def main():

    print("\n================================")
    print("QWEN TOKENIZER TEST")
    print("================================")

    loader = (
        QwenTokenizerLoader()
    )

    tokenizer = loader.load()

    text = (
        "What causes high latency "
        "in a 5G radio access network?"
    )

    tokens = tokenizer.encode(
        text
    )

    print(
        f"\nText:\n{text}"
    )

    print(
        f"\nToken Count: {len(tokens)}"
    )

    print(
        "\nTokenizer test passed."
    )


if __name__ == "__main__":

    main()