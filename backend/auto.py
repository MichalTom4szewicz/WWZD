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

ap = argparse.ArgumentParser()
ap.add_argument("-model", "--model", type=str, default="vgg16",
                help="name of pre-trained network to use")
args = vars(ap.parse_args())

# define a dictionary that maps model names to their classes
# inside Keras
MODELS = {
    "vgg16": VGG16,
    "vgg19": VGG19,
    "inception": InceptionV3,
    "xception": Xception,  # TensorFlow ONLY
    "resnet": ResNet50
}
# esnure a valid model name was supplied via command line argument
if args["model"] not in MODELS.keys():
    raise AssertionError("The --model command line argument should "
                         "be a key in the `MODELS` dictionary")


inputShape = (224, 224)
preprocess = imagenet_utils.preprocess_input
if args["model"] in ("inception", "xception"):
    inputShape = (299, 299)
    preprocess = preprocess_input


print("[INFO] loading {}...".format(args["model"]))
Network = MODELS[args["model"]]
model = Network(weights="imagenet")


f = open("info.txt", "w")

directory = './data/'
for filename in os.listdir(directory):
    image = load_img(directory + filename, target_size=inputShape)
    image = img_to_array(image)
    image = preprocess(image)

    #image = cv2.resize(img,(224,224))
    image = image.reshape(1,224,224,3)
    # classify the image
    preds = model.predict(image)
    P = imagenet_utils.decode_predictions(preds)
    # write as list
    f.write(str(P[0]) + '\n')
    # write in easy to read form
    #f.write(filename + ': ')
    #for (i, (imagenetID, label, prob)) in enumerate(P[0]):
    #    f.write("{}. {}: {:.2f}%".format(i + 1, label, prob * 100))
    #f.write("\n")

f.close()


