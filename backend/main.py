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
import joblib
from multiprocessing import Value
import time

from umap import UMAP

counter = Value('i', 0)
classes = ['pickup', 'sports_car', 'minivan']

method = "pca"
model = ResNet50(weights="imagenet")
resnet = ResNet50(include_top=False, weights="imagenet", pooling="avg")
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

def take_3_most_common_labels(feats):
    car_types = {}
    for i in range(len(feats)):
        for j in range(len(feats[0])):
            if (feats[i][j][1] in car_types):
                car_types[feats[i][j][1]] = car_types[feats[i][j][1]] + 1
            else:
                car_types[feats[i][j][1]] = 1
    car_types = dict(sorted(car_types.items(), reverse=True, key=lambda item: item[1]))
    keys = list(car_types.keys())
    return keys[:3]

def compare_images(feats, classes):
    coordinates = [[0 for x in range(len(classes))] for y in range(len(feats))]
    for item in range(len(feats)):
        for classIndex in range(len(classes)):
            for result in range(len(feats[0])):
                if (classes[classIndex] == feats[item][result][1]):
                    coordinates[item][classIndex] = feats[item][result][2]
    norm_coordinates = Normalizer(norm='l2').fit_transform(coordinates)
    print(norm_coordinates)
    return(norm_coordinates)

    # ???
def get_umap_norm(feats):
    normalizer_first = Normalizer(norm='l2')
    normalizer_first.fit(feats)
    norm_feats = normalizer_first.transform(feats)
    joblib.dump(normalizer_first, 'models/normalizer_first_umap.joblib')

    umap = UMAP(n_components=3, init='random', random_state=0)
    umap.fit(norm_feats)
    umap_feats = umap.transform(norm_feats)
    joblib.dump(umap, 'models/umap.joblib')

    normalizer_second = Normalizer(norm='l2')
    normalizer_second.fit(umap_feats)
    norm_feats = normalizer_second.transform(umap_feats)
    joblib.dump(normalizer_second, 'models/normalizer_second_umap.joblib')

    return norm_feats

    # ???
def transform_feats_umap(feats):
    normalizer_first = joblib.load('models/normalizer_first_umap.joblib')
    norm_feats = normalizer_first.transform(feats)

    umap = joblib.load('models/umap.joblib')
    umap_feats = umap.transform(norm_feats)

    normalizer_second = joblib.load('models/normalizer_second_umap.joblib')
    norm_feats = normalizer_second.transform(umap_feats)

    return norm_feats

def get_feats(model, input_shape, filename):
    image = load_img(filename, target_size=input_shape)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = imagenet_utils.preprocess_input(image)
    return model.predict(image)


def get_pca_norm(feats):
    normalizer_first = Normalizer(norm='l2')
    normalizer_first.fit(feats)
    norm_feats = normalizer_first.transform(feats)
    joblib.dump(normalizer_first, 'models/normalizer_first.joblib')

    pca = PCA(n_components=3, whiten=True)
    pca.fit(norm_feats)
    pca_feats = pca.transform(norm_feats)
    joblib.dump(pca, 'models/pca.joblib')

    normalizer_second = Normalizer(norm='l2')
    normalizer_second.fit(pca_feats)
    norm_feats = normalizer_second.transform(pca_feats)
    joblib.dump(normalizer_second, 'models/normalizer_second.joblib')

    return norm_feats


def transform_feats(feats):
    normalizer_first = joblib.load('models/normalizer_first.joblib')
    norm_feats = normalizer_first.transform(feats)

    pca = joblib.load('models/pca.joblib')
    pca_feats = pca.transform(norm_feats)

    normalizer_second = joblib.load('models/normalizer_second.joblib')
    norm_feats = normalizer_second.transform(pca_feats)

    return norm_feats


@app.route('/imgs', methods=['GET'])
def get_coordinates():
    value_pca = {}
    value_umap = {}
    if (os.path.exists('coords.json')):
        with open('coords.json') as json_file:
            coords = json.load(json_file)
            value_pca = {
                "status": "ready",
                "data": coords
            }
            # return json.dumps(value)
    if (os.path.exists('coords_umap.json')):
        with open('coords_umap.json') as json_file:
            coords = json.load(json_file)
            value_umap = {
                "status": "ready",
                "data": coords
            }
            # return json.dumps(value)

    if method == 'pca' and value_pca:
        return json.dumps(value_pca)
    elif method == 'umap' and value_umap:
        return json.dumps(value_umap)

    feats = []
    filenames = []

    for filename in glob.glob('imgs/*'):
        feats.append(get_feats(resnet, input_shape, filename))
        filenames.append(filename.split(sep="\\")[1])

    print("___________________PCA___________________")

    feats = np.reshape(feats, (len(filenames), 2048))
    norm_feats = get_pca_norm(feats)

    coords = []
    for i in range(len(filenames)):
        x, y, z = norm_feats[i]
        tmp = {
            "x": np.float64(x),
            "y": np.float64(y),
            "z": np.float64(z),
            "filename": filenames[i]
        }
        coords.append(tmp)

    with open('coords.json', 'w') as json_file:
        json.dump(coords, json_file)

    value_pca = {
        "status": "ready",
        "data": coords
    }
    #########################

    feats = []
    filenames = []

    for filename in glob.glob('imgs/*'):
        feats.append(get_feats(resnet, input_shape, filename))
        filenames.append(filename.split(sep="\\")[1])

    print("___________________UMAP___________________")

    feats = np.reshape(feats, (len(filenames), 2048))
    norm_feats = get_umap_norm(feats)
    # umap_3d = UMAP(n_components=3, init='random', random_state=0)
    # proj_3d = umap_3d.fit_transform(feats)
    # print(proj_3d)

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

    with open('coords_umap.json', 'w') as json_file:
        json.dump(obs, json_file)

    value_umap = {
        "status": "ready",
        "data": obs
    }

    if method == 'pca':
        return json.dumps(value_pca)
    elif method == 'umap':
        return json.dumps(value_umap)



@app.route('/file', methods=['POST'])
def handle_file():
    print(request.files)
    f = request.files['file']
    path = 'imgs/'
    ext = f.filename.split(".")[1]
    name_count = len(os.listdir(path)) + 1
    filename = secure_filename(f"img{name_count}.{ext}")
    path = os.path.join(path, filename)
    f.save(path)

    value_pca = {}
    value_umap = {}
    if (os.path.exists('coords.json')):
        with open('coords.json') as json_file:
            coords = json.load(json_file)

        # resnet = ResNet50(include_top=False, weights="imagenet", pooling="avg")
        # input_shape = (224, 224)
        feats = get_feats(resnet, input_shape, path)
        norm_feats = transform_feats(feats)

        x, y, z = norm_feats[0]
        tmp = {
            "x": np.float64(x),
            "y": np.float64(y),
            "z": np.float64(z),
            "filename": filename
        }
        coords.append(tmp)

        with open('coords.json', 'w') as json_file:
            json.dump(coords, json_file)

        value_pca = {
            "status": "ready",
            "data": coords
        }

        # return json.dumps(value)
    if (os.path.exists('coords_umap.json')):
        with open('coords_umap.json') as json_file:
            coords = json.load(json_file)

        # resnet = ResNet50(include_top=False, weights="imagenet", pooling="avg")
        # input_shape = (224, 224)
        feats = get_feats(resnet, input_shape, path)
        norm_feats = transform_feats_umap(feats)

        x, y, z = norm_feats[0]
        tmp = {
            "x": np.float64(x),
            "y": np.float64(y),
            "z": np.float64(z),
            "filename": filename
        }
        coords.append(tmp)

        with open('coords_umap.json', 'w') as json_file:
            json.dump(coords, json_file)

        value_umap = {
            "status": "ready",
            "data": coords
        }

        # return json.dumps(value)

    if not(os.path.exists('coords_umap.json') or os.path.exists('coords.json')):
        return get_coordinates()

    if method == 'pca':
        return json.dumps(value_pca)
    elif method == 'umap':
        return json.dumps(value_umap)


@app.route('/check', methods=['GET'])
def handle_check():
    global method
    return json.dumps({
        "method": method
    })


@app.route('/axes', methods=['POST'])
def post_axes():
    data = request.data.decode("utf-8")
    data = json.loads(data)

    global classes
    classes = data['axes']
    return get_class_coordinates()


@app.route('/method', methods=['POST'])
def handle_method():

    data = request.data.decode("utf-8")
    data = json.loads(data)

    global method
    method = data['method']

    time.sleep(1)
    return get_coordinates()# if method == 'pca' else get_umap_cords()


@app.route('/class', methods=['GET'])
def get_class_coordinates():

    feats = []
    filenames = []

    for filename in glob.glob('imgs/*.*'):
        feats.append(imagenet_utils.decode_predictions(get_feats(model, input_shape, filename)))
        filenames.append(filename.split(sep="\\")[1])
    print("___________________Class___________________")

    feats = np.squeeze(feats)
    class_coordinates = compare_images(feats, classes)

    obs = []
    for i in range(len(filenames)):
        x, y, z = class_coordinates[i]
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


# @app.route('/umap', methods=['GET'])
# def get_umap_cords():
#     if (os.path.exists('coords_umap.json')):
#         with open('coords_umap.json') as json_file:
#             coords = json.load(json_file)
#             value = {
#                 "status": "ready",
#                 "data": coords
#             }
#             return json.dumps(value)
#     else:
#         feats = []
#         filenames = []

#         for filename in glob.glob('imgs/*.*'):
#             feats.append(get_feats(resnet, input_shape, filename))
#             filenames.append(filename.split(sep="\\")[1])

#         print("___________________UMAP___________________")

#         feats = np.reshape(feats, (len(filenames), 2048))
#         norm_feats = get_umap_norm(feats)
#         # umap_3d = UMAP(n_components=3, init='random', random_state=0)
#         # proj_3d = umap_3d.fit_transform(feats)
#         # print(proj_3d)

#         obs = []
#         for i in range(len(filenames)):
#             x, y, z = norm_feats[i]
#             tmp = {
#                 "x": np.float64(x),
#                 "y": np.float64(y),
#                 "z": np.float64(z),
#                 "filename": filenames[i]
#             }
#             obs.append(tmp)

#         with open('coords_umap.json', 'w') as json_file:
#             json.dump(obs, json_file)

#         value = {
#             "status": "ready",
#             "data": obs
#         }

#         return json.dumps(value)


if __name__ == '__main__':

    app.run(debug=True, port=5000)
