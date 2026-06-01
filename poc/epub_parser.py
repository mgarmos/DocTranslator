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

        # Agregar el estado de traducción a cada elemento
        text_elements_con_traduccion = [[path, text, "N"] for path, text in text_elements]

        return text_elements_con_traduccion

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
        """
        Recorre el árbol y extrae tanto .text como .tail preservando espacios significativos.
        - Para .text usa la ruta normal: /tag[idx]/...
        - Para .tail añade la entrada con sufijo '/tail()' en la ruta correspondiente.
        """
        text_elements = []
        for idx, child in enumerate(element.iterchildren(), start=1):
            current_path = self._build_path(child, path, idx)

            # Extraer .text del child preservando espacios si son significativos
            if child.text is not None:
                text_content = child.text
                # Solo agregar si hay contenido no vacío (incluso si es solo espacios significativos)
                if text_content.strip():  # Hay contenido real
                    text_elements.append((current_path, text_content))
                elif text_content:  # Solo espacios, pero podrían ser significativos
                    # Preservar espacios entre elementos inline
                    text_elements.append((current_path, text_content))

            # Recorrer hijos recursivamente
            text_elements.extend(self.get_text_elements_with_path(child, current_path))

            # Capturar .tail (texto inmediatamente después del child)
            if child.tail is not None:
                tail_content = child.tail
                if tail_content.strip():  # Hay contenido real
                    tail_path = current_path + '/tail()'
                    text_elements.append((tail_path, tail_content))
                elif tail_content:  # Solo espacios, pero podrían ser significativos
                    tail_path = current_path + '/tail()'
                    text_elements.append((tail_path, tail_content))

        return text_elements

    def modify_document_with_text_elements(self, element, text_elements, path=''):
        """
        Recorre y reemplaza tanto .text como .tail de forma segura.
        Se espera que las entradas de text_elements que correspondan a tails tengan rutas terminadas en '/tail()'.
        """
        # Crear un diccionario para búsqueda más eficiente
        text_dict = {text_path: (new_text, traduccion) for text_path, new_text, traduccion in text_elements}
        
        for idx, child in enumerate(element.iterchildren(), start=1):
            current_path = self._build_path(child, path, idx)

            # Buscar y reemplazar .text
            if current_path in text_dict:
                new_text, traduccion = text_dict[current_path]
                child.text = new_text

            # Recursión en hijos
            self.modify_document_with_text_elements(child, text_elements, current_path)

            # Buscar y reemplazar .tail
            tail_key = current_path + '/tail()'
            if tail_key in text_dict:
                new_text, traduccion = text_dict[tail_key]
                child.tail = new_text

    def _build_path(self, element, path, idx):
        """Construye la ruta XPath del elemento de forma consistente."""
        tag_name = element.tag.split("}")[-1] if '}' in element.tag else element.tag
        return f'{path}/{tag_name}[{idx}]'

def main(ejecucion=1):
    # Ruta del archivo EPUB
    epub_path = 'poc/Examples/52 Weekly Affirmations_ Techniques to Unle - Joseph Murphy.epub'
    #epub_path = 'poc/Examples/Prueba.epub'
    
    # Crear una instancia del EPUBParser
    parser = EPUBParser()

    if ejecucion == 1:
    
        # Extraer texto del EPUB
        print("Extrayendo texto del EPUB...")
        text_elements = parser.extract_text(epub_path)
        
        # Mostrar el texto extraído
        for path, text, estadoTraduccion in text_elements:
            print(f'Ruta: {path}, Texto: {text} traducido: {estadoTraduccion}')

        # Guardar los elementos extraídos en un archivo JSON
        json_file_path = 'poc/Examples/text_elements.json'
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(text_elements, json_file, ensure_ascii=False, indent=4)            

    else:
    
        # Leer el json traducido
        json_file_path_mod = 'poc/Examples/text_elements_modificado.json'
        with open(json_file_path_mod, 'r', encoding='utf-8') as json_file:
            text_elements = json.load(json_file)
                
        # Modificar el documento
        print("\nModificando el EPUB...")
        parser.modify_document(epub_path, text_elements)
        print("El EPUB ha sido modificado y guardado como 'modified_book.epub'.")

if __name__ == "__main__":
    ejecucion = 2
    main(ejecucion)
