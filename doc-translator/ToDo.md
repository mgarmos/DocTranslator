# TODO

- Diseñar un json que lleve metadatos para poder controlar que se está parseando el ebook correcto
  - Generar hash del documento
  - Titulo, autor, etc

- Ver como se puede trocear una cadena si es mayor de 5000
- Ver como se pueden eliminar las cadenas de números o una unica letra
- Ver si se pueden agrupar los párrafos. Traducir parrafos consecutivos debería ayudar a la hora de traducir al tener mayor contexto

- Generar estadisticas de las llamdas a google para ver cuando comienza a fallar
  - Fallo a las 2100 cadenas

- Implemnetar pruebas unitarias

- No está traducindo las listas ->
    ```
        <div class="top1">
            <p class="hang1"><img alt="" height="15" src="docimages/a1.jpg" width="15"/>   If it interferes with your potential, it’s Self 1.</p>
            <p class="hang1"><img alt="" height="15" src="docimages/a1.jpg" width="15"/>   If it expresses your potential, it’s Self 2.</p>
        </div>
      
  ```

# Implementado

- Diseñar el json para que contenga la informacion de que textos se han llegado a traducir y cuales están pendientes
- Generar estadisticas de las llamdas a google para ver cuando comienza a fallar
