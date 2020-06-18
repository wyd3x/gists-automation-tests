from enum import Enum


class HTTPMethod(Enum):
    put = "PUT"
    get = "GET"
    post = "POST"
    patch = "PATCH"
    delete = "DELETE"
