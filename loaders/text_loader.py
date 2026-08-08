from loaders.base_loader import BaseLoader
from models.document import Document


class TextLoader(BaseLoader):
    def load(self, file_path: str) -> Document:
        '''Load text data from a file.'''
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

            return Document(
                content=text,
                metadata={
                    "source": file_path,
                    "type": "text"
                }
            )