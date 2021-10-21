# import the necessary packages
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.applications import Xception  # TensorFlow ONLY
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications import VGG19
from tensorflow.keras.applications import imagenet_utils
from tensorflow.keras.applications.inception_v3 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
import numpy as np
import argparse
import cv2
import os

# read from file to list    P[image][results][data]
P = [['' for x in range(15)] for y in range(100)]
characters_to_remove = "()[]' \n"
i = 0

f = open("info.txt", "r")

for line in f:
    for character in characters_to_remove:
        line = line.replace(character, "")
    P[i] = line.split(',')
    P[i] = np.reshape(P[i], (5, 3))
    i = i + 1

f.close()

# count how often certain feat appeared
car_types = {}

for i in range(100):
    for j in range(5):
        if (P[i][j][1] in car_types):
            car_types[P[i][j][1]] = car_types[P[i][j][1]] + 1
        else:
            car_types[P[i][j][1]] = 1

print(car_types)


