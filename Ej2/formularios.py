import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# Importar funciones necesarias
from funciones import *



# Imagen individual
"""
imagen = cv2.imread('./formulario_01.png', 0)
validarFormulario(imagen)

"""

# Todos los archivos que terminan en .png
directory = './'  # Directorio actual
image_files = [f for f in os.listdir(directory) if f.endswith('.png')]
#print(image_files)
x=1
for filename in image_files:
    image_path = os.path.join(directory, filename)
    imagen = cv2.imread(image_path, 0)
    #print(f"Formulario {x}:")
    print(filename)
    validarFormulario(imagen)
    x+=1
