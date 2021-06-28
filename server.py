#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request
import os
from flask import render_template
from engine import speech2text
from audioUtils import standard_file
import asyncio
import time
app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def index():
    return render_template("demo.html")

@app.route('/recog', methods=['GET', 'POST'])
def recog_file():
    if request.method == 'POST':
        static_file = request.files['the_file']
        # here you can send this static_file to a storage service
        # or save it permanently to the file system
        filename = '/tmp/' + static_file.filename
        static_file.save(filename)
        standard_file(filename)
        pred = speech2text()
        return pred

if __name__ == "__main__":
    app.debug=False
    app.run(host='0.0.0.0', port=5001, ssl_context=('cert.pem', 'key.pem'))
