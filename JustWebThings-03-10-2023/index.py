#!/usr/bin/env python3

import jwt
import os

from flask import Flask, request, Response, redirect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["50000 per hour"],
    storage_uri="memory://",
)


secret = os.urandom(32)

def get_new_cookie():
    return jwt.encode({"user": "normal"}, secret, algorithm="HS256")

def check_cookie(cookie):
    return jwt.decode(cookie, options={"verify_signature": False}, algorithms="HS256").get("user", "") == "admin"

@app.route('/')
@limiter.limit("5/second")
def index():
    return Response(open(__file__).read(), mimetype="text/plain")

@app.route('/docker')
@limiter.limit("5/second")
def docker():
    return Response(open("Dockerfile").read(), mimetype="text/plain")

@app.route('/flag')
@limiter.limit("5/second")
def flag_endpoint():
    if "token" not in request.cookies:
        ret = redirect("/flag")
        ret.set_cookie("token", get_new_cookie())
        return ret
    if check_cookie(request.cookies.get("token")):
        return open("flag.txt").read()
    else:
        return "Only admins can view the flag!"
    
if __name__ == "__main__":
    app.run('0.0.0.0', 11002)
