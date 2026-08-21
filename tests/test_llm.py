from llms.base_llm import BaseLLM


class FakeLLM(BaseLLM):

    def generate(self, messages: list[dict]) -> str:
        return "Python is a programming language."


def test_llm():
    llm = FakeLLM()

    messages = [
        {
            "role": "user",
            "content": "What is Python?",
        }
    ]

    response = llm.generate(messages)

    print("LLM response:")
    print(response)

    assert isinstance(response, str)
    assert response == "Python is a programming language."