from abc import ABC, abstractmethod

class BaseLLM(ABC):

    @abstractmethod
    def generate(self, messages: list[dict]) -> str:
        '''Generate a response from the Language Model.'''
        pass

from abc import ABC, abstractmethod


class BaseLLM(ABC):
    """
    Abstract interface for language model implementations.
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate a response from the given prompt.
        """
        raise NotImplementedError