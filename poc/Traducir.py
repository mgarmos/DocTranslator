from deep_translator import GoogleTranslator
import json

# Ruta del archivo JSON que contiene los textos extraídos
json_file_path_ini = 'poc/Examples/text_elements.json'
json_file_path_mod = 'poc/Examples/text_elements_modificado.json'

# 1. Leer los elementos desde el archivo JSON
with open(json_file_path_ini, 'r', encoding='utf-8') as json_file:
    text_elements = json.load(json_file)

# 2. Traducir cada texto y actualizar la lista
try:
    contador = 0
    for idx, (path, text) in enumerate(text_elements):
        translated_text = GoogleTranslator(source='english', target='spanish').translate(text)  # Traducir el texto
        text_elements[idx] = (path, translated_text)  # Actualizar el texto traducido
        contador += 1

        if contador % 100 == 0:
            print(f'avance {contador}')

except Exception as e:
    print(f"Error al traducir el texto en la ruta {path}: {e}")

print(f'Final: {contador}')

# 3. Guardar los textos traducidos de nuevo en el archivo JSON
with open(json_file_path_mod, 'w', encoding='utf-8') as json_file:
    json.dump(text_elements, json_file, ensure_ascii=False, indent=4)

# Imprimir los textos originales y traducidos
# for path, text in text_elements:
#     print(f"Ruta: {path}, Texto traducido: {text}")