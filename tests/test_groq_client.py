from llms.groq_client import GroqClient


def test_groq_client():

    llm = GroqClient()

    messages = [
        {
            "role": "user",
            "content": "In one sentence, what is Python?",
        }
    ]

    response = llm.generate(messages)

    print("\nGroq response:")
    print(response)

    assert isinstance(response, str)
    assert len(response.strip()) > 0