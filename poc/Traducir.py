from deep_translator import GoogleTranslator
import json
import time
from tqdm import tqdm

# Ruta del archivo JSON que contiene los textos extraídos
json_file_path_ini = 'poc/Examples/text_elements.json'
json_file_path_mod = 'poc/Examples/text_elements_modificado.json'

# 1. Leer los elementos desde el archivo JSON
with open(json_file_path_ini, 'r', encoding='utf-8') as json_file:
    text_elements = json.load(json_file)

# 2. Traducir cada texto y actualizar la lista
total_textos = len(text_elements)
traducidos = 0
inicio = time.time()
max_intentos = 5
intentos = 0
while intentos < max_intentos:
    try:
        for idx, (path, text, traduccion) in tqdm(enumerate(text_elements), total=total_textos):
            if traduccion is None or traduccion == "N":
                translated_text = GoogleTranslator(source='english', target='spanish').translate(text)  # Traducir el texto
                text_elements[idx] = (path, translated_text,  "T")  # Actualizar el texto traducido y el estado de traducción
                traducidos += 1
                tiempo_transcurrido = time.time() - inicio
                porcentaje = (idx + 1) / total_textos * 100                
                print(f"\rTraducidos {traducidos}/{total_textos} textos ({porcentaje:.2f}%) - Tiempo transcurrido: {tiempo_transcurrido:.2f} segundos", end='')
            tiempo_transcurrido = time.time() - inicio
            print(f"Tiempo transcurrido: {tiempo_transcurrido:.2f} segundos", end='\r')
        break  # Sale del while si no ocurre un error
    except Exception as e:
        intentos += 1
        print(f"Error en la traducción: {e}")
        print(f"Intento {intentos}/{max_intentos}")
        # Volver a cargar la lista text_elements desde el archivo JSON
        with open(json_file_path_ini, 'r', encoding='utf-8') as json_file:
            text_elements = json.load(json_file)

# 3. Guardar los textos traducidos de nuevo en el archivo JSON
with open(json_file_path_mod, 'w', encoding='utf-8') as json_file:
    json.dump(text_elements, json_file, ensure_ascii=False, indent=4)

print(f"Traducción completada en {time.time() - inicio:.2f} segundos")