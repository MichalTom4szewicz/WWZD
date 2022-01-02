import json
from logging import debug
import random
from sklearn.decomposition import PCA
from tensorflow.keras.applications import ResNet50, imagenet_utils
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from sklearn.preprocessing import Normalizer
from keras.models import Model
from werkzeug.utils import secure_filename
from flask import request
from flask import Flask
from flask_cors import CORS
from PIL import Image
from numpy import asarray
import numpy as np
import math
import glob
import os, os.path
from multiprocessing import Value
import time

from umap import UMAP

counter = Value('i', 0)

method = "pca"
model = ResNet50(weights="imagenet")
global_avg_pool = Model(model.inputs, model.get_layer(index=175).output)
input_shape = (224, 224)

app = Flask(__name__)
CORS(app)


def geeks():
    language = "Python"
    company = "GeeksForGeeks"
    Itemid = 1
    price = 0.00

    value = {
        "language": language,
        "company": company,
        "Itemid": Itemid,
        "price": price
    }

    return json.dumps(value)


def to_gray(img):
    gray_img = []
    w, h, d = img.shape

    for row in img:
        for elem in row:
            r = 0
            b = 0
            g = 0
            if d == 4:
                r, g, b, a = elem
            else:
                r, g, b = elem
            gray = (r/255 + g/255 + b/255)/3*255
            gray_img.append(math.floor(gray))

    # gray_img
    np_gray = np.array(gray_img)
    return np_gray  # .reshape((w, h))


def file_coordinates():
    value = {
        "x": 10,
        "y": 31,
        "z": 1,
    }

    return json.dumps(value)


@app.route("/")
def hello_world():
    return geeks()

@app.route("/testInit")
def init_chart():
    classes = [
      "car",
      "bus",
      "jeep",
      "truck",
      "minibus",
      "plane",
      "sportscar",
      "pickup",
      "minivan",
      "limousine",
      "train",
    ]
    randomCords = []
    for c in classes:
        randomCords.append([random.randint(0, 20), random.randint(0, 20), random.randint(0, 20), c])
        randomCords.append([random.randint(0, 20), random.randint(0, 20), random.randint(0, 20), c])

    return json.dumps(randomCords)


def get_feats(model, input_shape, filename):
    image = load_img(filename, target_size=input_shape)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = imagenet_utils.preprocess_input(image)
    return model.predict(image)


def get_pca_norm(feats):
    pca = PCA(n_components=3, whiten=True)
    pca_feats = pca.fit_transform(feats)
    print(pca_feats)

    norm_feats = Normalizer(norm='l2').fit_transform(pca_feats)
    print(norm_feats)

    return norm_feats


@app.route('/imgs', methods=['GET'])
def get_coordinates():

    feats = []
    filenames = []

    for filename in glob.glob('imgs/*.*'):
        feats.append(get_feats(global_avg_pool, input_shape, filename))
        filenames.append(filename.split(sep="\\")[1])
    print("___________________PCA___________________")

    if (len(filenames) > 3):
        feats = np.reshape(feats, (len(filenames), 2048))
        norm_feats = get_pca_norm(feats)

        obs = []
        for i in range(len(filenames)):
            x, y, z = norm_feats[i]
            tmp = {
                "x": np.float64(x),
                "y": np.float64(y),
                "z": np.float64(z),
                "filename": filenames[i]
            }
            obs.append(tmp)

        value = {
            "status": "ready",
            "data": obs
        }

        return json.dumps(value)

    return json.dumps({"status": "not-ready"})


@app.route('/file', methods=['POST'])
def handle_file():
    print(request.files)
    f = request.files['file']
    path = 'imgs/'

    ext = f.filename.split(".")[1]
    name_count = len(os.listdir(path)) + 1
    with counter.get_lock():
        f.save(os.path.join(path, secure_filename(f"img{name_count}.{ext}")))

    return get_coordinates() if method == 'pca' else get_umap_cords()


@app.route('/check', methods=['GET'])
def handle_check():
    global method
    return json.dumps({
        "method": method
    })


@app.route('/method', methods=['POST'])
def handle_method():

    data = request.data.decode("utf-8")
    data = json.loads(data)

    global method
    method = data['method']

    time.sleep(1)
    # return json.dumps({
    #     "method": method
    # })
    return get_coordinates() if method == 'pca' else get_umap_cords()


@app.route('/umap', methods=['GET'])
def get_umap_cords():

    feats = []
    filenames = []

    for filename in glob.glob('imgs/*.*'):
        feats.append(get_feats(global_avg_pool, input_shape, filename))
        filenames.append(filename.split(sep="\\")[1])

    print("___________________UMAP___________________")

    feats = np.reshape(feats, (len(filenames), 2048))

    umap_3d = UMAP(n_components=3, init='random', random_state=0)
    proj_3d = umap_3d.fit_transform(feats)

    print(proj_3d)

    obs = []
    for i in range(len(filenames)):
        x, y, z = proj_3d[i]
        tmp = {
            "x": np.float64(x),
            "y": np.float64(y),
            "z": np.float64(z),
            "filename": filenames[i]
        }
        obs.append(tmp)

    value = {
        "status": "ready",
        "data": obs
    }

    return json.dumps(value)

    # return json.dumps({"status": "not-ready"})

    return json.dumps({
        "method": method
    })



if __name__ == '__main__':

    app.run(debug=True, port=5000)
