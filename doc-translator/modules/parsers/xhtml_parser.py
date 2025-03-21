from lxml import etree
from .document_parser import DocumentParser

class XHTMLParser(DocumentParser):
    def parse(self, content):
        """Parses the XHTML content and returns the root element."""
        return etree.fromstring(content)

    def extract_text(self, content):
        """Extracts text elements from the XHTML content."""
        tree = self.parse(content)
        return self.get_text_elements_with_path(tree)

    def modify_document(self, content, text_elements):
        """Modifies the XHTML document based on the provided text elements."""
        tree = self.parse(content)
        self.modify_document_with_text_elements(tree, text_elements)
        return etree.tostring(tree, pretty_print=True, encoding='utf-8').decode('utf-8')


    def get_text_elements_with_path(self, element, path=''):
        """
        Extrae los textos de los elementos en el árbol XML/XHTML junto con sus rutas.

        :param element: El elemento XML/XHTML actual.
        :param path: La ruta acumulada del elemento actual.
        :return: Una lista de tuplas que contienen la ruta y el texto de los elementos.
        """
        text_elements = []

        # Iterar sobre todos los elementos hijos del árbol
        for idx, child in enumerate(element.iterchildren(), start=1):
            # Construir la ruta utilizando el método común
            current_path = self._build_path(child, path, idx)
            
            # Comprobar si el elemento tiene texto
            if child.text and child.text.strip():
                text_elements.append((current_path, child.text.strip()))  # Empaquetar en una tupla

            # Llamar recursivamente para los hijos
            text_elements.extend(self.get_text_elements_with_path(child, current_path))
        
        return text_elements

    def modify_document_with_text_elements(self, element, text_elements, path=''):
        # (Implementación del método ya existente)
        """
        Modifica el texto de los elementos en el árbol XML/XHTML basado en las rutas y textos proporcionados.

        :param element: El elemento XML/XHTML actual.
        :param text_elements: Lista de tuplas que contienen rutas y nuevos textos.
        :param path: La ruta acumulada del elemento actual.
        :return: La lista de text_elements (sin cambios).
        """
        # Iterar sobre todos los elementos hijos del árbol
        for idx, child in enumerate(element.iterchildren(), start=1):
            # Construir la ruta utilizando el método común
            current_path = self._build_path(child, path, idx)

            # Comprobar si la ruta está en text_elements
            for text_path, new_text in text_elements:
                if current_path == text_path:
                    # Modificar el texto del elemento
                    child.text = new_text
                    break  # Salir del bucle al encontrar la coincidencia


            # Llamar recursivamente para los hijos
            self.modify_document_with_text_elements(child, text_elements, current_path)
        
        return text_elements

    def _build_path(self, element, path, idx):
        """
        Construye la ruta de un elemento en el árbol XML/XHTML.

        :param element: El elemento XML/XHTML actual.
        :param path: La ruta acumulada del elemento actual.
        :param idx: El índice del elemento hijo.
        :return: La ruta construida.
        """
        return f'{path}/{element.tag.split("}")[-1]}[{idx}]' if '}' in element.tag else f'{path}/{element.tag}[{idx}]'