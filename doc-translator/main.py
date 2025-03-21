import json
import os
from modules.parsers import XHTMLParser

class DocumentManager:
    @staticmethod
    def load_document(file_path):
        with open(file_path, 'rb') as f:
            return f.read()
       

    @staticmethod
    def save_document(file_path, content):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    @staticmethod
    def load_json(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def save_json(file_path, data):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

def main(ejecutar=1):
    # Rutas de los archivos
    xhtml_file_path = 'poc/Examples/ejemplo.xhtml'
    json_output_path = 'poc/Examples/text_elements.json'
    json_input_path = 'poc/Examples/text_elements_modificado.json'
    modified_xhtml_file_path = 'poc/Examples/ejemplo_modificado.xhtml'

    # Instanciar el parser
    parser = XHTMLParser()


    # 1. Cargar el documento XHTML y extraer textos
    content = DocumentManager.load_document(xhtml_file_path)
    text_elements = parser.extract_text(content)
    
    if ejecutar == 1:

        # Guardar los elementos de texto en un archivo JSON
        DocumentManager.save_json(json_output_path, text_elements)

        print(f"Textos extraídos y guardados en {json_output_path}")
    
    else:

        # 2. Cargar el JSON de elementos de texto modificados
        modified_text_elements = DocumentManager.load_json(json_input_path)

        # Modificar el documento XHTML
        modified_content = parser.modify_document(content, modified_text_elements)

        # Guardar el documento modificado
        DocumentManager.save_document(modified_xhtml_file_path, modified_content)

        print(f"Documento modificado guardado en {modified_xhtml_file_path}")

if __name__ == "__main__":
    ejecutar = 2
    main(ejecutar)
