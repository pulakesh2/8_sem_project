from application import app
from flask import render_template,url_for,request, redirect
import secrets
import os

import cv2
import pytesseract
import numpy as np

@app.route("/")
def index():
    return render_template("index.html",title="Home Page")

@app.route("/upload", methods=["POST","GET"])
def upload():
    if request.method == "POST":

        sentence = ""

        f = request.files.get("file")
        filename,extension = f.filename.split(".")
        generate_filename = secrets.token_hex(20) + f" .{extension}"

        file_location = os.path.join(app.config["UPLOADED_PATH"],generate_filename)
        f.save(file_location)

        # error line
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR/tesseract.exe'

        img = cv2.imread(file_location)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

        boxes = pytesseract.image_to_data(img)

        for i,box in enumerate(boxes.splitlines()):
            if i == 0:
                continue

            box = box.split()

            if len(box) == 12:
                sentence += box[11] + " "
            
        print(sentence)

        os.remove(file_location)

        return redirect("/decoded/")

    else:
        return render_template("upload.html", title="Upload")



@app.route("/decoded", methods=["POST","GET"])
def decoded():
    return "Hello world"