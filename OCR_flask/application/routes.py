from application import app
from flask import render_template,url_for,request, redirect,session
from application.forms import MyForm
from application import utils
import secrets
import os


import cv2
import pytesseract
import numpy as np
from gtts import gTTS

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
            
        # print(sentence)
        session["sentence"] = sentence

        os.remove(file_location)

        return redirect("/decoded/")

    else:
        return render_template("upload.html", title="Upload")



@app.route("/decoded", methods=["POST","GET"])
def decoded():
    sentence = session.get("sentence")
    form = MyForm()
    if request.method == "POST":

        generated_audio_filename = secrets.token_hex(10) + ".mp4"

        text_data = form.text_field.data
        translate_to = form.language_field.data
        # print("Translate to: ", translate_to)

        translated_text = utils.translate_text(text_data,translate_to)

        # print(translated_text)
        form.text_field.data = translated_text
        tts = gTTS(translated_text,lang=translate_to)

        file_location = os.path.join(app.config["AUDIO_FILE_UPLOAD"],generated_audio_filename)


        tts.save(file_location)


        return render_template("decoded.html", title="Translations" , form = form, audio = True, file = generated_audio_filename)

    else:
        form.text_field.data = sentence
        session["sentence"] = ""
        return render_template("decoded.html", form = form, audio = False)