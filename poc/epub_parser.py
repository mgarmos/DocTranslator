import ebooklib
from ebooklib import epub
from lxml import etree
import json


class EPUBParser():
    def parse(self, content):
        """Parses the EPUB content and returns the root element."""
        book = epub.read_epub(content)     
        return book

    def extract_text(self, content):
        """Extracts text elements from the EPUB content."""
        book = self.parse(content)
        text_elements = []
        
        for index, item in enumerate(book.get_items_of_type(ebooklib.ITEM_DOCUMENT), start=1):
            tree = etree.fromstring(item.get_content())           
            text_elements.extend(self.get_text_elements_with_path(tree, index))
        
        return text_elements

    def modify_document(self, content, text_elements):
        """Modifies the EPUB document based on the provided text elements."""
        book = self.parse(content)
        
        for index, item in enumerate(book.get_items_of_type(ebooklib.ITEM_DOCUMENT), start=1):
            tree = etree.fromstring(item.get_content())
            self.modify_document_with_text_elements(tree, text_elements, index)
            item.set_content(etree.tostring(tree, pretty_print=True, encoding='utf-8').decode('utf-8'))
        
        # Guardar el libro modificado en un nuevo archivo EPUB
        epub.write_epub('poc/Examples/modified_book.epub', book)

    def get_text_elements_with_path(self, element, path=''):
        text_elements = []
        for idx, child in enumerate(element.iterchildren(), start=1):
            current_path = self._build_path(child, path, idx)
            if child.text and child.text.strip():
                text_elements.append((current_path, child.text.strip()))
            text_elements.extend(self.get_text_elements_with_path(child, current_path))
        return text_elements

    def modify_document_with_text_elements(self, element, text_elements, path=''):
        for idx, child in enumerate(element.iterchildren(), start=1):
            current_path = self._build_path(child, path, idx)
            for text_path, new_text in text_elements:
                if current_path == text_path:
                    child.text = new_text
                    break
            self.modify_document_with_text_elements(child, text_elements, current_path)

    def _build_path(self, element, path, idx):
        return f'{path}/{element.tag.split("}")[-1]}[{idx}]' if '}' in element.tag else f'{path}/{element.tag}[{idx}]'

def main(ejecucion=1):
    # Ruta del archivo EPUB
    epub_path = 'poc/Examples/The Inner Game of Music - Barry Green.epub'
    
    # Crear una instancia del EPUBParser
    parser = EPUBParser()

    if ejecucion == 1:
    
        # Extraer texto del EPUB
        print("Extrayendo texto del EPUB...")
        text_elements = parser.extract_text(epub_path)
        
        # Mostrar el texto extraído
        for path, text in text_elements:
            print(f'Ruta: {path}, Texto: {text}')

        # 2. Guardar los elementos extraídos en un archivo JSON
        json_file_path = 'poc/Examples/text_elements.json'
        with open(json_file_path, 'w') as json_file:
            json.dump(text_elements, json_file, ensure_ascii=False, indent=4)            

    else:
    
        # 1. Leer el json traducido
        json_file_path_mod = 'poc/Examples/text_elements_modificado.json'
        with open(json_file_path_mod, 'r', encoding='utf-8') as json_file:
            text_elements = json.load(json_file)
                
        # # Modificar el documento
        print("\nModificando el EPUB...")
        parser.modify_document(epub_path, text_elements)
        print("El EPUB ha sido modificado y guardado como 'modified_book.epub'.")

if __name__ == "__main__":
    ejecucion = 1
    main(ejecucion)
