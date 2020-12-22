#!/usr/bin/env python

# pylint: disable=C0103,C0114,C0115,C0116,R0903

from fastapi import FastAPI, Request
from waitress import serve
import os
import json

from function import handler

app = FastAPI()


class Event:
    def __init__(self, request: Request):
        self.body = request.json()
        self.headers = request.headers
        self.method = request.method
        self.query = request.args
        self.path = request.path


class Context:
    def __init__(self):
        self.hostname = os.getenv("HOSTNAME", "localhost")


def format_status_code(resp):
    if "statusCode" in resp:
        return resp["statusCode"]

    return 200


def format_body(resp):
    if "body" not in resp:
        return ""
    elif isinstance(resp["body"], dict):
        return json.dumps(resp["body"])
    return str(resp["body"])


def format_headers(resp):
    if "headers" not in resp:
        return []
    elif isinstance(resp["headers"], dict):
        headers = []
        for key in resp["headers"].keys():
            header_tuple = (key, resp["headers"][key])
            headers.append(header_tuple)
        return headers

    return resp["headers"]


def format_response(resp):
    if resp == None:
        return ("", 200)

    statusCode = format_status_code(resp)
    body = format_body(resp)
    headers = format_headers(resp)

    return (body, statusCode, headers)


@app.get("/")
@app.post("/")
@app.put("/")
def call_handler(path):
    event = Event()
    context = Context()
    response_data = handler.handle(event, context)

    resp = format_response(response_data)
    return resp


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)
