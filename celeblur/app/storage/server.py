import os

from flask import Flask, request

from embedding_storage import EmbeddingStorage

global emb_storage
emb_storage = EmbeddingStorage()

app = Flask(__name__)


@app.route("/emb/add", methods=["POST"])
def emb_add():
    emb = request.json["emb"]
    name = request.json["name"]
    emb_storage.add(emb, name)
    return {}


@app.route("/emb/find_match", methods=["POST"])
def emb_k_nbrs():
    emb = request.json["emb"]
    tol = request.json.get("tol", 0.6)
    name = emb_storage.find_match(emb, tol)
    return {"name": name}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ["PORT"]))
