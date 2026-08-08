from abc import ABC, abstractmethod
from models.document import Document
class BaseLoader(ABC):

    @abstractmethod
    def load(self, file_path: str) -> Document:
        '''Load data into the system.'''
        pass