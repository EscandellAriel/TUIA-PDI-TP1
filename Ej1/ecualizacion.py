import cv2
import numpy as np
import matplotlib.pyplot as plt

def local_histogram_equalization(image, window_alto, window_ancho):
    # Obtener las dimensiones de la imagen
    height, width = image.shape

    # Inicializar una imagen de salida
    output_image = np.zeros_like(image)

    # Copiar la imagen original en la imagen de salida
    output_image = np.copy(image)

    # Dividir la imagen con bordes ampliados en ventanas y aplicar ecualización del histograma en cada ventana
    imagen_bordes = add_border(image, window_alto // 2, window_alto // 2, window_ancho // 2, window_ancho // 2)
    
    # Recorrer la imagen con bordes ampliados
    for i in range(0+window_alto//2, height + window_alto // 2,1):
        for j in range(0+window_ancho//2, width + window_ancho//2,1):
            # Definir la ventana en la imagen con bordes ampliados
            window = imagen_bordes[i-window_alto//2:i+window_alto//2, j-window_ancho//2:j+window_ancho//2]
            # Aplicar la ecualización del histograma en la ventana
            equalized_window = cv2.equalizeHist(window)

            # Asignar el valor central de la ventana ecualizada a la imagen de salida (imagen original)
            output_image[i - window_alto // 2, j - window_ancho // 2] = equalized_window[window_alto // 2, window_ancho // 2]
        
    return output_image

# Función para agregar un borde a la imagen
def add_border(image, top, bottom, left, right):
    return cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_REPLICATE)

# Cargar la imagen a procesar
image = cv2.imread('./Imagen_con_detalles_escondidos.tif', cv2.IMREAD_GRAYSCALE)

# Especificar el tamaño de la ventana de procesamiento
window_alto = 10
window_ancho = 10

# Tamaños de prueba de la ventana de procesamiento
window_alto_1 = 15
window_ancho_1 = 15

window_alto_2 = 20
window_ancho_2 = 20

window_alto_3 = 30
window_ancho_3 = 30

# Aplicar la ecualización local del histograma
result_image = local_histogram_equalization(image, window_alto, window_ancho)

# Aplicar la ecualización local del histograma a las pruebas

result_image_1 = local_histogram_equalization(image, window_alto_1, window_ancho_1)

result_image_2 = local_histogram_equalization(image, window_alto_2, window_ancho_2)

result_image_3 = local_histogram_equalization(image, window_alto_3, window_ancho_3)

# Imagen ecualizada completa

equalized_window = cv2.equalizeHist(image)

#-----------# GRAFICOS #-----------#

# Imagen original y ecualizacion de histograma en imagen completa

ax1 = plt.subplot(121)
plt.imshow(image,cmap='gray')
plt.title('Imagen Original')

plt.subplot(122,sharex=ax1,sharey=ax1)
plt.imshow(equalized_window,cmap='gray')
plt.title('Imagen completamente ecualizada')

plt.show()


# Sub plots de comparacion tamanio de kernels 10, 15, 20 y 30

ax1 = plt.subplot(221)
plt.imshow(result_image,cmap='gray')
plt.title('kernel 10 x 10')

plt.subplot(222,sharex=ax1,sharey=ax1)
plt.imshow(result_image_1,cmap='gray')
plt.title('kernel 15 x 15')

plt.subplot(223,sharex=ax1,sharey=ax1)
plt.imshow(result_image_2,cmap='gray')
plt.title('kernel 20 x 20')

plt.subplot(224,sharex=ax1,sharey=ax1)
plt.imshow(result_image_3,cmap='gray')
plt.title('kernel 30 x 30')

plt.show()


# Sub plots de la imagen original y la mejor ecualizacion de histograma

ax1 = plt.subplot(121)
plt.imshow(image,cmap='gray')
plt.title('Imagen Original')

plt.subplot(122,sharex=ax1,sharey=ax1)
plt.imshow(result_image_2,cmap='gray')
plt.title('Imagen localmente ecualizada kernel 20 x 20')

plt.show()
