# DocTranslater

## 1. **Descripción General del Proyecto**

El objetivo es desarrollar una aplicación que permita traducir libros electrónicos (eBooks) de un idioma a otro. La aplicación debe ser capaz de:

1. Navegar por la estructura del eBook.
2. Determinar las cadenas de texto a traducir.
3. Llamar a un servicio de traducción y obtener los resultados.
4. Insertar las cadenas traducidas en la ubicación correspondiente dentro del eBook.

La estructura del proyecto debe ser modular desde el inicio para facilitar la escalabilidad y el mantenimiento.

---

## 2. **Requisitos Funcionales**

### 2.1 **Manejo de eBooks**
- Leer eBooks en formato EPUB (soporte inicial).
- Extraer el texto navegable y los metadatos del eBook.
- Posibilidad de añadir soporte a otros formatos (como PDF) en el futuro.

### 2.2 **Traducción**
- Integrar con una API de traducción (inicialmente, Google Translate a través de `googletrans` o la API oficial de Google Cloud).
- Soporte para múltiples idiomas (detectar automáticamente el idioma origen).

### 2.3 **Gestión de la Cola de Traducción**
- Implementar un sistema de cola para manejar las llamadas a la API de traducción.
- Registrar el progreso de las traducciones, indicando:
  - El índice de la última cadena traducida exitosamente.
  - El texto traducido.
- Permitir reanudar el proceso desde el punto en que se detuvo.

### 2.4 **Reemplazo de Texto**
- Reemplazar las cadenas traducidas en la estructura del eBook.
- Preservar el formato y la estructura original.

---

## 3. **Requisitos No Funcionales**

### 3.1 **Arquitectura Modular**
El proyecto debe dividirse en módulos claramente diferenciados según sus funcionalidades principales:
- Manejo de eBooks.
- Traducción (interacción con la API).
- Gestión de la cola de traducción.
- Inserción de cadenas traducidas.

### 3.2 **Escalabilidad**
- Permitir agregar soporte para nuevos formatos de eBooks y servicios de traducción.
- Manejar grandes volúmenes de texto eficientemente.

### 3.3 **Manejo de Errores**
- Registrar errores en un log para facilitar la depuración.
- Proveer mensajes claros en caso de fallos, especialmente en la interacción con la API de traducción.

### 3.4 **Persistencia de Datos**
- Guardar la cola de traducción en un archivo (por ejemplo, JSON) para reanudar el trabajo.
- Registrar el progreso en un archivo de log.

---

## 4. **Estructura Propuesta del Proyecto**
```plaintext
ebook-translator/
├── main.py                 # Punto de entrada principal de la aplicación.
├── modules/                # Módulos funcionales organizados.
│   ├── parser.py           # Manejo de la estructura del ebook (navegación y extracción de texto).
│   ├── translator.py       # Lógica de traducción (gestión de la cola de llamadas y API de traducción).
│   ├── replacer.py         # Reemplazo del texto traducido en el ebook.
│   ├── queue_manager.py    # Gestión de la cola y registro de progreso.
│   ├── utils.py            # Utilidades compartidas (funciones auxiliares, logs, etc.).
├── data/                   # Archivos relacionados con el progreso y datos temporales.
│   ├── translation_queue.json  # Cola de traducción serializada.
│   ├── progress.log         # Registro del progreso de la traducción.
├── tests/                  # Tests para cada módulo.
│   ├── test_parser.py
│   ├── test_translator.py
│   ├── test_replacer.py
│   ├── test_queue_manager.py
├── requirements.txt        # Dependencias del proyecto.
├── poc/                    # Proof of Concept - 
└── README.md               # Documentación inicial del proyecto.
