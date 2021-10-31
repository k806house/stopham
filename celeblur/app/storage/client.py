from urllib.parse import urljoin

import requests


class StorageClient:
    def __init__(self, url):
        self.url = url

    def emb_add(self, emb, name):
        response = requests.post(urljoin(self.url, "emb/add"),
                                 json={
                                     "emb": emb.tolist(),
                                     "name": name
                                 })

    def emb_find_match(self, emb, tol):
        response = requests.post(urljoin(self.url, "emb/find_match"),
                                 json={
                                     "emb": emb.tolist(),
                                     "tol": tol,
                                 })
        data = response.json()

        return data["name"]
