import json
from logging import debug

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
from multiprocessing import Value

counter = Value('i', 0)

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


@app.route('/file', methods=['POST'])
def handle_file():

    numba = 4
    # data = request.get_json()

    print(request.files)
    f = request.files['file']

    # f.save(secure_filename(f.filename))
    ext = f.filename.split(".")[1]
    with counter.get_lock():
        # counter.value += 1

        f.save(secure_filename(f"img{counter.value}.{ext}"))
        counter.value += 1
        val = counter.value

    if val > numba-1:

        model = ResNet50(weights="imagenet")
        global_avg_pool = Model(model.inputs, model.get_layer(index=175).output)
        inputShape = (224, 224)

        feats = []
        for i in range(val):
            image = load_img(f"img{i}.{ext}", target_size=inputShape)
            image = img_to_array(image)
            image = np.expand_dims(image, axis=0)
            image = imagenet_utils.preprocess_input(image)
            features = global_avg_pool.predict(image)
            feats.append(features)

        feats = np.reshape(feats, (val, 2048))

        pca = PCA(n_components=3, whiten=True)
        pca_feats = pca.fit_transform(feats)
        print(pca_feats)

        norm_feats = Normalizer(norm='l2').fit_transform(pca_feats)
        print(norm_feats)

        # n = []
        # for pair3 in norm_feats:
        #     x, y, z = pair3
        #     if(x < 0):
        #         x = math.log10(abs(int(x)))
        #         x *= -1
        #     else:
        #         x = math.log10(abs(int(x)))

        #     if(y < 0):
        #         y = math.log10(abs(int(y)))
        #         y *= -1
        #     else:
        #         y = math.log10(abs(int(y)))

        #     if(z < 0):
        #         z = math.log10(abs(int(z)))
        #         z *= -1
        #     else:
        #         z = math.log10(abs(int(z)))

        #     pair = x, y, z
        #     n.append(pair)

        # print(n)

        # obs = []
        # for i in range(val):
        #     x, y, z = n[i]
        #     tmp = {
        #         "x": x,
        #         "y": y,
        #         "z": z
        #     }
        #     obs.append(tmp)

        # value = {
        #     "status": "ready",
        #     "data": obs
        # }

        # return json.dumps(value)

    # image = Image.open(f"img.{ext}")

    # image_data = asarray(image)

    # gray = to_gray(image_data)
    # gray = np.array([gray])

    # print(gray.shape)

    # pca = PCA(0.8)
    # # gray = gray.reshape(1, -1)
    # p_comp = pca.fit_transform(gray)

    # print(p_comp.shape)

    # return file_coordinates()
    return json.dumps({"status": "not-ready"})


if __name__ == '__main__':

    app.run(debug=True, port=5000)
