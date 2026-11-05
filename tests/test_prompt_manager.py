from llm.prompt_manager.telecom_qa_prompt import (
    TelecomQAPrompt
)

from llm.prompt_manager.rca_prompt import (
    RCAPrompt
)

from llm.prompt_manager.optimization_prompt import (
    OptimizationPrompt
)


def test_telecom_prompt():

    query = (
        "What causes high latency in a "
        "5G radio access network?"
    )

    context = (
        "[Evidence 1]\n"
        "Dataset: TeleLogs\n"
        "Source: TeleLogs\n"
        "Content:\n"
        "High Latency | Low Throughput\n"
        "Root Cause: Congestion"
    )

    prompt_manager = TelecomQAPrompt()

    prompt = prompt_manager.build(
        query=query,
        context=context
    )

    if not prompt.strip():
        raise AssertionError(
            "Telecom prompt is empty."
        )

    if query not in prompt:
        raise AssertionError(
            "Query is missing from telecom prompt."
        )

    if context not in prompt:
        raise AssertionError(
            "Context is missing from telecom prompt."
        )

    print("\n================================")
    print("TELECOM PROMPT")
    print("================================")
    print(prompt)


def test_rca_prompt():

    query = (
        "Why is the cell experiencing "
        "high latency and low throughput?"
    )

    context = (
        "[Evidence 1]\n"
        "Dataset: TeleLogs\n"
        "Source: TeleLogs\n"
        "Content:\n"
        "High Latency | Low Throughput\n"
        "Root Cause: Congestion"
    )

    prompt_manager = RCAPrompt()

    prompt = prompt_manager.build(
        query=query,
        context=context
    )

    if not prompt.strip():
        raise AssertionError(
            "RCA prompt is empty."
        )

    if query not in prompt:
        raise AssertionError(
            "Query is missing from RCA prompt."
        )

    if context not in prompt:
        raise AssertionError(
            "Context is missing from RCA prompt."
        )

    print("\n================================")
    print("RCA PROMPT")
    print("================================")
    print(prompt)


def test_optimization_prompt():

    query = (
        "How can the network reduce "
        "congestion and improve throughput?"
    )

    context = (
        "[Evidence 1]\n"
        "Dataset: TeleLogs\n"
        "Source: TeleLogs\n"
        "Content:\n"
        "High Latency | Low Throughput\n"
        "Root Cause: Congestion"
    )

    prompt_manager = OptimizationPrompt()

    prompt = prompt_manager.build(
        query=query,
        context=context
    )

    if not prompt.strip():
        raise AssertionError(
            "Optimization prompt is empty."
        )

    if query not in prompt:
        raise AssertionError(
            "Query is missing from "
            "optimization prompt."
        )

    if context not in prompt:
        raise AssertionError(
            "Context is missing from "
            "optimization prompt."
        )

    print("\n================================")
    print("OPTIMIZATION PROMPT")
    print("================================")
    print(prompt)


def main():

    print("\n================================")
    print("PROMPT MANAGER TEST")
    print("================================")

    test_telecom_prompt()

    test_rca_prompt()

    test_optimization_prompt()

    print("\n================================")
    print("PROMPT MANAGER TEST PASSED")
    print("================================")


if __name__ == "__main__":
    main()