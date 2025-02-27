import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

# Definir la función para leer un archivo EPUB
def leer_ebook(ruta_archivo):
    # Abrir el archivo EPUB
    libro = epub.read_epub(ruta_archivo)
    
    # Inicializar una lista para almacenar el texto
    textos = []
    
    # Iterar sobre cada documento del libro
    for doc in libro.get_items():
        # Verificar si el documento es un archivo HTML
        if doc.get_type() == ebooklib.ITEM_DOCUMENT:
            # Parsear el HTML utilizando BeautifulSoup
            soup = BeautifulSoup(doc.get_content().decode('utf-8'), 'html.parser')
            
            # Extraer el texto de todo el documento
            texto = soup.get_text()
            
            # Agregar el texto a la lista
            textos.append(texto)
    
    # Retornar la lista de textos
    return textos

# Definir la ruta del archivo EPUB
ruta_archivo1 = 'poc/Examples/example_ebook.epub'
ruta_archivo2 = 'poc/Examples/zenstudiespodcast.epub'

# Leer el archivo EPUB y almacenar el texto en una lista
textos = leer_ebook(ruta_archivo1)

# Imprimir el texto
print('---- INICIO ----------')
for texto in textos:
    print(texto)

# ToDo's para mejorar la implementación:
# 1. **Mejorar la extracción de texto**: La función `get_text()` de BeautifulSoup puede extraer texto de manera poco eficiente. Investigar formas de mejorar la extracción de texto.
# 2. **Manejar errores**: Agregar manejo de errores para casos en los que el archivo EPUB no se pueda abrir o leer.
# 3. **Soportar múltiples formatos**: Agregar soporte para leer archivos EPUB en diferentes formatos (por ejemplo, EPUB 2, EPUB 3, etc.).
# 4. **Mejorar la estructura del código**: Reorganizar el código para que sea más modular y fácil de mantener.
# 5. **Soportar archivos EPUB con imágenes**: Agregar soporte para leer archivos EPUB que contienen imágenes y otros medios.
# 6. **Mejorar la documentación**: Agregar documentación para explicar cómo utilizar la función `leer_ebook()` y cómo procesar el texto extraído.
