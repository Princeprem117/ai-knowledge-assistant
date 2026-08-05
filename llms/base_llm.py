from abc import ABC, abstractmethod

class BaseLLM(ABC):

    @abstractmethod
    def generate(self, messages: list[dict]) -> str:
        '''Generate a response from the Language Model.'''
        pass