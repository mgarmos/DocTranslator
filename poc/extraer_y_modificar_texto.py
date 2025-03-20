from lxml import etree

# Este script tiene como objetivo manipular un documento XHTML.
# Realiza las siguientes operaciones:
# 1. Carga un documento XHTML desde un archivo.
# 2. Extrae los textos de todos los elementos del documento junto con sus rutas.
# 3. Modifica los textos extraídos añadiendo " Modificado" al final de cada uno.
# 4. Aplica las modificaciones al documento original.
# 5. Guarda el documento modificado en un nuevo archivo.

# Función para extraer rutas y textos de un documento
def get_text_elements_with_path(element, path=''):
    """
    Extrae los textos de los elementos en el árbol XML/XHTML junto con sus rutas.

    :param element: El elemento XML/XHTML actual.
    :param path: La ruta acumulada del elemento actual.
    :return: Una lista de tuplas que contienen la ruta y el texto de los elementos.
    """
    text_elements = []

    # Iterar sobre todos los elementos hijos del árbol
    for idx, child in enumerate(element.iterchildren(), start=1):
        # Construir la ruta sin el espacio de nombres
        current_path = f'{path}/{child.tag.split("}")[-1]}[{idx}]' if '}' in child.tag else f'{path}/{child.tag}[{idx}]'
        
        # Comprobar si el elemento tiene texto
        if child.text and child.text.strip():
            text_elements.append((current_path, child.text.strip()))  # Empaquetar en una tupla

        # Llamar recursivamente para los hijos
        text_elements.extend(get_text_elements_with_path(child, current_path))
    
    return text_elements

# Función para modificar el documento basado en text_elements
def modify_document_with_text_elements(element, text_elements, path=''):
    """
    Modifica el texto de los elementos en el árbol XML/XHTML basado en las rutas y textos proporcionados.

    :param element: El elemento XML/XHTML actual.
    :param text_elements: Lista de tuplas que contienen rutas y nuevos textos.
    :param path: La ruta acumulada del elemento actual.
    :return: La lista de text_elements (sin cambios).
    """
    # Iterar sobre todos los elementos hijos del árbol
    for idx, child in enumerate(element.iterchildren(), start=1):
        # Construir la ruta sin el espacio de nombres
        current_path = f'{path}/{child.tag.split("}")[-1]}[{idx}]' if '}' in child.tag else f'{path}/{child.tag}[{idx}]'
        
        # Comprobar si la ruta está en text_elements
        for text_path, new_text in text_elements:
            if current_path == text_path:
                # Modificar el texto del elemento
                child.text = new_text

        # Llamar recursivamente para los hijos
        modify_document_with_text_elements(child, text_elements, current_path)
    
    return text_elements

# Cargar el documento XHTML
with open('poc/Examples/ejemplo.xhtml', 'rb') as file: 
    tree = etree.parse(file)

# 1. Extraer rutas y textos
text_elements = get_text_elements_with_path(tree.getroot())  # Llamar a getroot()

# 2. Imprimir los elementos extraídos
print('Elementos extraídos:')
for path, text in text_elements:
    print(f'Ruta: {path}, Texto: {text}')

# 3. Modifico text_elements
lista_temporal = []
for tupla in text_elements:
    nuevo_texto = tupla[1] + ' Modificado'  # Añadir " Modificado" al texto original
    nueva_tupla = (tupla[0], nuevo_texto)  # Crear una nueva tupla con la ruta y el nuevo texto
    lista_temporal.append(nueva_tupla)

# Reemplazar la lista original con la nueva lista
text_elements = lista_temporal    

# 4. Modificar el documento
modify_document_with_text_elements(tree.getroot(), text_elements)

# 5. Guardar el documento modificado (opcional)
with open('poc/Examples/ejemplo_modificado.xhtml', 'wb') as file:
    file.write(etree.tostring(tree, pretty_print=True, encoding='utf-8'))

print("El documento ha sido modificado y guardado con éxito")
