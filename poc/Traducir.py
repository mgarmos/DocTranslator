from deep_translator import GoogleTranslator
import json
import time
from tqdm import tqdm

# Ruta del archivo JSON que contiene los textos extraídos
json_file_path_ini = 'poc/Examples/text_elements.json'
json_file_path_mod = 'poc/Examples/text_elements_modificado.json'

# Separador único que no aparecerá en los textos
SEPARADOR = " |||SEP||| "

# 1. Leer los elementos desde el archivo JSON
with open(json_file_path_ini, 'r', encoding='utf-8') as json_file:
    text_elements = json.load(json_file)

# 2. Preparar textos para traducción por lotes
total_textos = len(text_elements)
traducidos = 0
inicio = time.time()
max_intentos = 5
intentos = 0

# Tamaño máximo del lote (en caracteres, considerando límite de Google Translate)
MAX_BATCH_SIZE = 4500  # Dejamos margen respecto al límite de 5000

while intentos < max_intentos:
    try:
        # Agrupar textos pendientes de traducir
        textos_pendientes = []
        indices_pendientes = []
        
        for idx, (path, text, traduccion) in enumerate(text_elements):
            if traduccion is None or traduccion == "N":
                textos_pendientes.append(text)
                indices_pendientes.append(idx)
        
        if not textos_pendientes:
            print("No hay textos pendientes de traducir.")
            break
        
        # Procesar en lotes
        i = 0
        with tqdm(total=len(textos_pendientes), desc="Traduciendo") as pbar:
            while i < len(textos_pendientes):
                lote_actual = []
                indices_lote = []
                longitud_acumulada = 0
                
                # Construir lote respetando el límite de tamaño
                while i < len(textos_pendientes):
                    texto_actual = textos_pendientes[i]
                    longitud_texto = len(texto_actual) + len(SEPARADOR)
                    
                    if longitud_acumulada + longitud_texto > MAX_BATCH_SIZE and lote_actual:
                        break
                    
                    lote_actual.append(texto_actual)
                    indices_lote.append(indices_pendientes[i])
                    longitud_acumulada += longitud_texto
                    i += 1
                
                # Concatenar textos del lote con el separador
                texto_concatenado = SEPARADOR.join(lote_actual)
                
                # Traducir el lote completo
                traduccion_concatenada = GoogleTranslator(source='english', target='spanish').translate(texto_concatenado)
                
                # Separar las traducciones
                traducciones = traduccion_concatenada.split(SEPARADOR)
                
                # Actualizar los elementos traducidos
                for idx_original, traduccion in zip(indices_lote, traducciones):
                    path, _, _ = text_elements[idx_original]
                    text_elements[idx_original] = (path, traduccion.strip(), "T")
                    traducidos += 1
                
                pbar.update(len(lote_actual))
                
                # Pequeña pausa para evitar límites de tasa
                time.sleep(0.1)
        
        break  # Sale del while si no ocurre un error
        
    except Exception as e:
        intentos += 1
        print(f"\nError en la traducción: {e}")
        print(f"Intento {intentos}/{max_intentos}")
        
        # Volver a cargar la lista text_elements desde el archivo JSON
        with open(json_file_path_ini, 'r', encoding='utf-8') as json_file:
            text_elements = json.load(json_file)
        
        if intentos < max_intentos:
            time.sleep(2)  # Esperar antes de reintentar

# 3. Guardar los textos traducidos de nuevo en el archivo JSON
with open(json_file_path_mod, 'w', encoding='utf-8') as json_file:
    json.dump(text_elements, json_file, ensure_ascii=False, indent=4)

tiempo_total = time.time() - inicio
print(f"\nTraducción completada: {traducidos} textos en {tiempo_total:.2f} segundos")
print(f"Promedio: {tiempo_total/traducidos:.3f} segundos por texto")
