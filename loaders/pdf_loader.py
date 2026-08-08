from loaders.base_loader import BaseLoader

class PdfLoader(BaseLoader):
    def load(self, file_path: str) -> str:
        '''Load PDF data from a file.'''
        # Implement PDF loading logic here
        # For example, you can use PyPDF2 or pdfplumber to extract text from the PDF

        
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
            return text