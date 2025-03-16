"""
Este script en Python 3 utiliza la librería lxml para procesar y manipular contenido HTML.

Librerías utilizadas:
- lxml: Esta librería se utiliza para el análisis y manipulación de documentos XML y HTML. Proporciona una forma eficiente de trabajar con árboles de elementos y permite realizar consultas XPath.

Descripción del código:
1. Se define una cadena de texto que contiene un documento HTML estructurado.
2. Se parsea el contenido HTML utilizando `html.fromstring`, creando un árbol de elementos.
3. Se define un diccionario `resultados` para almacenar el texto extraído junto con sus rutas XPath correspondientes.
4. Se implementa una función recursiva `extraer_texto_y_xpath` que recorre el árbol de elementos, extrayendo el texto de cada elemento y almacenándolo en el diccionario con su ruta XPath.
5. Se llama a la función para iniciar la extracción de texto desde el elemento raíz del documento.
6. Se imprime el texto extraído junto con sus rutas XPath.
7. Se define un diccionario `nuevos_textos` que contiene nuevas cadenas de texto para reemplazar en el documento HTML original.
8. Se implementa la función `reemplazar_texto`, que busca elementos en el documento utilizando XPath y reemplaza su texto con el nuevo texto proporcionado en el diccionario.
9. Se llama a la función para realizar las sustituciones en el documento.
10. Finalmente, se convierte el documento modificado de nuevo a una cadena HTML y se imprime el resultado.

El propósito de este script es extraer texto de un documento HTML, modificarlo y luego mostrar el HTML resultante con los cambios aplicados.
"""


from lxml import html

# Cargar el contenido HTML
html_string = '''
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>Capitulo I</title>
</head>

<body>
    <h1>Capitulo 1</h1>
    <p>Ejemplo de capítulo primero, parrafo uno</p>
    <p>Ejemplo de capítulo primero, parrafo dos</p>
</body>
</html>
'''

# Parsear el HTML
document = html.fromstring(html_string)

# Diccionario para almacenar los resultados
resultados = {}

# Función recursiva para recorrer el árbol y extraer texto
def extraer_texto_y_xpath(elemento, ruta_actual):
    # Si el elemento tiene texto, lo almacenamos en el diccionario
    if elemento.text and elemento.text.strip():
        resultados[ruta_actual] = elemento.text.strip()
    
    # Recorremos los hijos del elemento
    for i, hijo in enumerate(elemento):
        # Construimos la ruta XPath para el hijo
        nueva_ruta = f"{ruta_actual}/{hijo.tag}[{i + 1}]"
        extraer_texto_y_xpath(hijo, nueva_ruta)
    
    # También verificamos el texto que puede estar en el final del elemento
    if elemento.tail and elemento.tail.strip():
        resultados[ruta_actual] = resultados.get(ruta_actual, '') + ' ' + elemento.tail.strip()

# Llamar a la función con el elemento raíz
extraer_texto_y_xpath(document, '/html')

# Imprimir los resultados
print("Texto extraído y sus rutas XPath:")
for xpath, texto in resultados.items():
    print(f"XPath: {xpath}, Texto: {texto}")

# Diccionario con nuevas sustituciones
nuevos_textos = {
    '/html/body/h1[1]': 'Capítulo 1 Modificado',
    '/html/body/p[1]': 'Ejemplo de capítulo primero, párrafo uno modificado',
    '/html/body/p[2]': 'Ejemplo de capítulo primero, párrafo dos modificado'
}

# Función para reemplazar el texto en el HTML
def reemplazar_texto(documento, diccionario):
    for xpath, nuevo_texto in diccionario.items():
        # Buscar el elemento usando XPath
        elementos = documento.xpath(xpath)
        if elementos:
            # Reemplazar el texto del primer elemento encontrado
            elementos[0].text = nuevo_texto

# Llamar a la función para reemplazar el texto
reemplazar_texto(document, nuevos_textos)

# Convertir el documento de nuevo a una cadena HTML
html_modificado = html.tostring(document, pretty_print=True, encoding='unicode')

# Imprimir el HTML modificado
print("\nHTML modificado:")
print(html_modificado)
