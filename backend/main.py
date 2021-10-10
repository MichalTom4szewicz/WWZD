import json
from logging import debug

from flask import Flask

app = Flask(__name__)


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
    # return "<p>Hello, World!</p>"


if __name__ == '__main__':
    app.run(debug=True)
