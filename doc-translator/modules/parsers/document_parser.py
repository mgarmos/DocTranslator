from abc import ABC, abstractmethod

class DocumentParser(ABC):
    @abstractmethod
    def parse(self, content):
        """Parses the content and returns the root element."""
        pass

    @abstractmethod
    def extract_text(self, content):
        """Extracts text elements from the content."""
        pass

    @abstractmethod
    def modify_document(self, content, text_elements):
        """Modifies the document based on the provided text elements."""
        pass
