import json
from logging import debug

from sklearn.decomposition import PCA
from werkzeug.utils import secure_filename
from flask import request
from flask import Flask
from flask_cors import CORS
from PIL import Image
from numpy import asarray
import numpy as np
import math


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
    return np_gray.reshape((w, h))


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
    # data = request.get_json()

    print(request.files)
    f = request.files['file']

    # f.save(secure_filename(f.filename))
    ext = f.filename.split(".")[1]
    f.save(secure_filename(f"img.{ext}"))

    image = Image.open(f"img.{ext}")

    image_data = asarray(image)

    gray = to_gray(image_data)

    pca = PCA(.95)
    pca.fit(gray)

    print(pca.explained_variance_ratio_)
    print(pca.singular_values_)

    return file_coordinates()


if __name__ == '__main__':
    app.run(debug=True, port=5000)
