from flask import Flask, render_template, request, jsonify
from palatio import palatio

import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

from PIL import Image
import io

import re
import spacy
from nltk.corpus import words

import pandas as pd
import itertools
import json


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index2.html')


@app.route('/output', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
       img = request.files['file'].read()
       raw_text = pytesseract.image_to_string(Image.open(io.BytesIO(img)))
       output = palatio(raw_text)
       return output


if __name__ == '__main__':
   app.run(debug=True)

