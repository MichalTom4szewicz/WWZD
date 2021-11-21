import json
from logging import debug

from flask import Flask
from flask_cors import CORS
from flask import request

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
    data = request.get_json()
    print(data)
    return file_coordinates()


if __name__ == '__main__':
    app.run(debug=True)
