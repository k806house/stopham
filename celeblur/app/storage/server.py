import os

from flask import Flask, request

from storage import Storage

global storage
storage = Storage()

app = Flask(__name__)


@app.route("/emb/add", methods=["POST"])
def emb_add():
    emb = request.json["emb"]
    name = request.json["name"]
    storage.add(emb, name)
    return {}


@app.route("/emb/find_match", methods=["POST"])
def emb_k_nbrs():
    emb = request.json["emb"]
    tol = request.json.get("tol", 0.6)
    name = storage.find_match(emb, tol)
    return {"name": name}


@app.route("/get_names", methods=["POST"])
def get_names():
    return {"names": storage.get_names()}


@app.route("/save", methods=["POST"])
def save():
    filename = request.json.get("filename", "dump")
    storage.save(filename)
    return {}


@app.route("/load", methods=["POST"])
def load():
    filename = request.json.get("filename", "dump")
    storage.load(filename)
    return {}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ["PORT"]))
