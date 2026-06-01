from deep_translator import GoogleTranslator
import json
import time
from tqdm import tqdm

# Ruta del archivo JSON que contiene los textos extraídos
json_file_path_ini = 'poc/Examples/text_elements.json'
json_file_path_mod = 'poc/Examples/text_elements_modificado.json'

# Parámetros de configuración
BATCH_SIZE = 50  # Guardar cada 50 traducciones
SAVE_INTERVAL = 60  # O guardar cada 60 segundos
MAX_INTENTOS = 5

def guardar_progreso(text_elements, file_path):
    """Guarda el progreso actual en el archivo JSON"""
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(text_elements, json_file, ensure_ascii=False, indent=4)

# 1. Leer los elementos desde el archivo JSON
with open(json_file_path_ini, 'r', encoding='utf-8') as json_file:
    text_elements = json.load(json_file)

# 2. Traducir cada texto y actualizar la lista
total_textos = len(text_elements)
traducidos = 0
inicio = time.time()
ultimo_guardado = time.time()
traducciones_desde_ultimo_guardado = 0

intentos = 0
while intentos < MAX_INTENTOS:
    try:
        for idx, (path, text, traduccion) in tqdm(enumerate(text_elements), total=total_textos):
            if traduccion is None or traduccion == "N":
                translated_text = GoogleTranslator(source='english', target='spanish').translate(text)
                text_elements[idx] = (path, translated_text, "T")
                traducidos += 1
                traducciones_desde_ultimo_guardado += 1
                
                # Guardar por lotes o por tiempo
                tiempo_actual = time.time()
                if (traducciones_desde_ultimo_guardado >= BATCH_SIZE or 
                    tiempo_actual - ultimo_guardado >= SAVE_INTERVAL):
                    guardar_progreso(text_elements, json_file_path_mod)
                    traducciones_desde_ultimo_guardado = 0
                    ultimo_guardado = tiempo_actual
                
                tiempo_transcurrido = time.time() - inicio
                porcentaje = (idx + 1) / total_textos * 100
                print(f"\rTraducidos {traducidos}/{total_textos} textos ({porcentaje:.2f}%) - Tiempo: {tiempo_transcurrido:.2f}s", end='')
            
            tiempo_transcurrido = time.time() - inicio
            print(f"Tiempo transcurrido: {tiempo_transcurrido:.2f} segundos", end='\r')
        
        break  # Sale del while si no ocurre un error
        
    except Exception as e:
        intentos += 1
        print(f"\nError en la traducción: {e}")
        print(f"Intento {intentos}/{MAX_INTENTOS}")
        
        # Guardar progreso antes de reintentar
        guardar_progreso(text_elements, json_file_path_mod)
        
        # Recargar desde el último guardado
        with open(json_file_path_mod, 'r', encoding='utf-8') as json_file:
            text_elements = json.load(json_file)

# 3. Guardar los textos traducidos finales
guardar_progreso(text_elements, json_file_path_mod)

print(f"\nTraducción completada en {time.time() - inicio:.2f} segundos")
