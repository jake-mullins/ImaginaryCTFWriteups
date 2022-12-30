#!/usr/bin/env python
from flask import Flask, request, Response, render_template, jsonify
import jsonschema
import requests
import json
import os

app = Flask(__name__, template_folder="/app")
app.config["SECRET_KEY"] = os.urandom(32)


productDB = None
with open("productDB.json", "r") as fd:
    productDB = json.loads(fd.read())

schema = {
    "type": "object",
    "properties": {
        "orderId": {
            "type": "number",
            "maximum": 10,
        },
        "cart": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "number",
                        "minimum": 0,
                        "exclusiveMaximum": len(productDB),
                    },
                    "qty": {"type": "integer", "minimum": 1},
                },
                "required": ["id", "qty"],
            },
        },
    },
    "required": ["orderId", "cart"],
}


@app.route("/", methods=["GET", "POST"])
def index():
    flash = None
    if request.method == "POST":
        data = request.get_json(force=True)
        try:
            jsonschema.validate(instance=data, schema=schema)
        except jsonschema.exceptions.ValidationError as e:
            return jsonify({"error": f"failed to validate {data}"})
        resp = requests.post("http://localhost:8000/process", data=request.get_data())

        if resp.status_code == 200:
            try:
                return resp.json()
            except requests.exceptions.JSONDecodeError:
                return jsonify({"resp": resp.text})
        else:
            return jsonify({"error": "Error during payment processing"})

    return render_template("index.html", products=productDB)


@app.route("/source")
def frontend():
    with open(__file__, "r") as f:
        source = f.read()
    return Response(source, mimetype="text/plain")


@app.route("/process")
def backend():
    with open("/app/process.go", "r") as f:
        source = f.read()
    return Response(source, mimetype="text/plain")


if __name__ == "__main__":
    app.run("0.0.0.0", 5000)
