import cv2
import numpy as np
import matplotlib.pyplot as plt

#-----------# SEGMENTACION DE LINEAS DEL FORMULARIO #-----------#

# Encontrar el inicio y el fin de las líneas horizontales y verticales

def find_start_end(arr):
    start = None
    end = None
    segments = []
    for i, val in enumerate(arr):
        if val and start is None:
            start = i
        elif not val and start is not None:
            end = i
            segments.append((start, end))
            start = None
            end = None
    return segments




#-----------# VALIDACION DE CONTENIDO #-----------#

# Validar las preguntas:
# Preguntas: se debe marcar con 1 caracter una de las dos celdas SI y NO.
# No pueden estar ambas vacías ni ambas completas.

def validarPreguntas(preguntas):
 texto = ""
 
 for key in preguntas.keys():
   if ((preguntas[key][2] + preguntas[key][4]) != 1):
     texto += f"{preguntas[key][0]}: MAL \n"
   else:
    texto += f"{preguntas[key][0]}: OK \n"

 return texto

#Validar los campos:

def validarCampos(formulario):
  texto = ""
  for campo in formulario.keys():
      if campo == 1: #Nombrey Apellido  Debe contener al menos 2 palabras y no más de 25 caracteres en total.
        #return (cantidad_comp <=25 and cantidad_palabras <=2)
        if (formulario[campo][2] <=25 and formulario[campo][3] >=2):
          texto += f"Nombre y Apellido: OK \n"
        else:
           texto += f"Nombre y Apellido: MAL \n"
      if campo == 2:  #Edad  Debe contener 2 o 3 caracteres.
        if (formulario[campo][2] <=3 and formulario[campo][2] >=2):
          texto += f"Edad: OK \n"
        else:
            texto +=f"Edad: MAL \n"
      if campo == 3: #Mail  Debe contener 1 palabra y no más de 25 caracteres.
        if (formulario[campo][2] <=25 and formulario[campo][3] <=1):
         texto +=f"Mail: OK \n"
        else:
            texto +=f"Mail: MAL \n"
      if campo == 4: #Legajo   8 caracteres formando 1 sola palabra.
        if (formulario[campo][2] ==8 and formulario[campo][3] <=1):
         texto +=f"Legajo: OK \n"
        else:
           texto +=f"Legajo: MAL \n"
      if campo == 9: #Comentario   No debe contener más de 25 caracteres.
        if (formulario[campo][2]<=25):
            texto +=f"Comentario: OK \n"
        else:
           texto +=f"Comentario: MAL \n"

  return texto



#-----------# VALIDACION DEL FORMULARIO #-----------#

def validarFormulario(imagen):

  # Aplicar umbral a la imagen
  umbral = 120  # Ajusta el umbral según tu imagen
  img_th = cv2.threshold(imagen, umbral, 255, cv2.THRESH_BINARY_INV)[1]
  #cv2.imshow(img_th)
  # Sumar los valores de los píxeles en cada columna y fila
  img_cols = np.sum(img_th, axis=0)
  img_rows = np.sum(img_th, axis=1)

  # Definir umbrales para detectar las líneas
  th_row = 0.75 * np.max(img_rows)
  th_col = 0.32 * np.max(img_cols)

  # Detectar las posiciones de las líneas horizontales y verticales
  img_rows_th = img_rows > th_row
  img_cols_th = img_cols > th_col

  # Encontrar segmentos de líneas horizontales y verticales
  rows_segments = find_start_end(img_rows_th)
  cols_segments = find_start_end(img_cols_th)

  # Dibujar líneas en la imagen original para visualizar los bordes
  imagen_color = cv2.cvtColor(img_th, cv2.COLOR_GRAY2BGR)

  for start, end in rows_segments:
      cv2.line(imagen_color, (0, start), (imagen.shape[1], start), (0, 0, 255), 2)

  for start, end in cols_segments:
      cv2.line(imagen_color, (start, 0), (start, imagen.shape[0]), (0, 0, 255), 2)

  #cv2.imshow(imagen_color)

  # Elimino los campos fijos del formulario
  rows_segments = rows_segments[1:]
  cols_segments = cols_segments[1:]

  filas3_cols = [4,5,6,7]

  formulario = {1:['Nombre y apelido'],2:['Edad'],3:['Mail'],4:['Legajo'],9:['Comentario']}
  preguntas = {6:['Pregunta 1'], 7:['Pregunta 2'],8:['Pregunta 3']}

  # Obtener las celdas y los caracteres dentro de cada celda de preguntas
  for i in range(5,8):
      for j in range(len(cols_segments) - 1):

          # Definir las coordenadas de la celda actual
          y1 = rows_segments[i][0]
          y2 = rows_segments[i + 1][1]
          x1 = cols_segments[j][0]
          x2 = cols_segments[j + 1][1]

          # Recortar la celda de la imagen
          celda_img = img_th[y1:y2, x1:x2]

          # Eliminar componentes conectadas pequeñas
          _, labels, stats, _ = cv2.connectedComponentsWithStats(celda_img, 8, cv2.CV_32S)
          preguntas[i+1].append(celda_img)

          # Definir un umbral de área para eliminar componentes pequeñas
          th_area = 5  # Ajusta este umbral hasta el punto =5

          cantidad_componentes = len(stats) - 2
          #print(f"fila {preguntas[i+1][0]}, columna {j+1} cant-comp:  {cantidad_componentes}")
          preguntas[i+1].append(cantidad_componentes)

          # Filtrar componentes por área
          ix_area = stats[:, -1] > th_area
          stats = stats[ix_area, :]

          # Dibujar un rectángulo alrededor de cada componente conectada
          for stat in stats:
              x, y, w, h, area = stat
              cv2.rectangle(imagen_color, (x + x1, y + y1), (x + x1 + w, y + y1 + h), (0, 255, 0), 2)


  for i in range(len(rows_segments) - 1):
      if i in filas3_cols:
        continue
      for j in range(len(cols_segments) - 1):
          if j == 1:
            continue
          # Definir las coordenadas de la celda actual
          y1 = rows_segments[i][0]
          y2 = rows_segments[i + 1][1]
          x1 = cols_segments[j][0]
          x2 = cols_segments[j + 2][1]

          # Recortar la celda de la imagen
          celda_img = img_th[y1:y2, x1:x2]

          formulario[i+1].append(celda_img)

          # Eliminar componentes conectadas pequeñas
          _, labels, stats, centroids = cv2.connectedComponentsWithStats(celda_img, 8, cv2.CV_32S)

          #print(stats, label)

          # Definir un umbral de área para eliminar componentes pequeñas
          th_area = 5  # Ajusta este umbral hasta el punto . = 5

          cantidad_componentes = len(stats) - 2
          #print(f"fila {formulario[i+1][0]}, cant-comp: {cantidad_componentes}")
          formulario[i+1].append(cantidad_componentes)

           # Filtrar componentes por área
          ix_area = stats[:, -1] > th_area
          stats = stats[ix_area, :]


          #Calcular el umbral de distancia entre componentes para separar palabras
          anchos=[]
          distancias=[]
          cantidad_palabras=0
          umbral_espacios=9
          #https://docs.opencv.org/3.4/d3/dc0/group__imgproc__shape.html

          conjuntos_componentes = []
          conjunto_actual = []
          conjunto_valores_especialesLegajo=[14,15,17]
          conjunto_valores_especielesMail=[10,11,19]

          # Iterar a través de las etiquetas de las componentes
          for label in range(2, len(stats)):
              componente = (labels == label).astype(np.uint8)

              if conjunto_actual:
                  # Calcular la distancia horizontal entre componentes
                  distancia_horizontal = stats[label, cv2.CC_STAT_LEFT] - (stats[label - 1, cv2.CC_STAT_LEFT] + stats[label - 1, cv2.CC_STAT_WIDTH])
                  #if i+1==3:
                    #print(f"distancia:{distancia_horizontal}")
                    #print(f"Altura{stats[label, cv2.CC_STAT_HEIGHT]}")
                  if distancia_horizontal >= umbral_espacios and distancia_horizontal <22 and  stats[label, cv2.CC_STAT_HEIGHT]>10:
                    # Reglas especiales para filtrar caracteres -,/,_ en los campos Mial y Legajo

                    if (i+1==4 and distancia_horizontal in conjunto_valores_especialesLegajo) or (i+1==3 and distancia_horizontal in conjunto_valores_especielesMail) :continue
                    else:
                      conjuntos_componentes.append(conjunto_actual)
                      conjunto_actual = []
                      espacios_entre_componentes = 0
                      #print(distancia_horizontal)

              conjunto_actual.append(componente)



          # Agregar el último conjunto si existe
          if conjunto_actual:
              conjuntos_componentes.append(conjunto_actual)
          # Imprimir la cantidad de conjuntos (palabras) para fines de validación
          cantidad_palabras = len(conjuntos_componentes)
          #if cantidad_componentes!=0:#si no esta vacio se considera al menos una palabra
          #   cantidad_palabras+=1

          #print("Cantidad de palabras:", cantidad_palabras)
          formulario[i+1].append(cantidad_palabras)


          # Dibujar un rectángulo alrededor de cada componente conectada
          for stat in stats:
              x, y, w, h, area = stat
              cv2.rectangle(imagen_color, (x + x1, y + y1), (x + x1 + w, y + y1 + h), (0, 255, 0), 2)
 
 # Mostrar la imagen con los bordes detectados y los caracteres resaltados

  ax1 = plt.subplot(121)
  plt.imshow(imagen, cmap='gray')
  plt.title('Formulario Original')

  plt.subplot(122, sharex=ax1, sharey=ax1)
  plt.imshow(imagen_color, cmap='gray')
  plt.title('Imagen procesada')

  # Texto para la primera función
  text_validar_campos = validarCampos(formulario)
  plt.text(1.2, -0.3, text_validar_campos, ha='left', va='center', transform=ax1.transAxes, bbox=dict(facecolor='white', alpha=0.8))

  # Texto para la segunda función
  text_validar_preguntas = validarPreguntas(preguntas)
  plt.text(1.7, -0.25, text_validar_preguntas, ha='center', va='center', transform=ax1.transAxes, bbox=dict(facecolor='white', alpha=0.8))
  
  plt.show()


