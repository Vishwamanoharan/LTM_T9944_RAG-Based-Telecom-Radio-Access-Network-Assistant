from llm.qwen_2_5.inference import (
    QwenInference
)


def main():

    print("\n================================")
    print("QWEN INFERENCE TEST")
    print("================================")

    llm = QwenInference()

    prompt = """
Explain what causes high latency in a 5G radio access network.
"""

    print("\nPrompt:")
    print(prompt)

    response = llm.generate(
        prompt=prompt,
        max_new_tokens=150
    )

    print("\n================================")
    print("MODEL RESPONSE")
    print("================================")

    print(response)

    print("\nInference test passed.")


if __name__ == "__main__":
    main()