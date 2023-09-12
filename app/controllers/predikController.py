from app import app
from flask import redirect, request, jsonify, render_template, session
import cv2
from tensorflow.keras.models import load_model
from time import sleep
from keras.preprocessing import image
from tensorflow.keras.utils import img_to_array
import numpy as np
import glob
import pandas as pd
import os
from werkzeug.utils import secure_filename
from app.models.historiModel import db, Histori
from flask_marshmallow import Marshmallow

ma = Marshmallow(app)


class HistoriSchema(ma.Schema):
    class Meta:
        fields = ('id', 'ruangan', 'mata_kuliah', 'kelas',
                  'tanggal', 'hasilSenang', 'hasilBiasa', 'id_dosen')


histori_schema = HistoriSchema()
historis_schema = HistoriSchema(many=True)

UPLOAD_FOLDER = 'images/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


face_classifier = cv2.CascadeClassifier(
    'model/haarcascade_frontalface_default.xml')
classifier = load_model('model/model.h5')

emotion_labels = ['Senang ', 'Biasa ']


def predict(image):
    deteksi = []
    for i in range(len(image)):
        gray = cv2.cvtColor(image[i], cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray)
        for (x, y, w, h) in faces:
            cv2.rectangle(image[i], (x, y), (x + w, y + h), (0, 255, 255), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_gray = cv2.resize(roi_gray, (48, 48),
                                  interpolation=cv2.INTER_AREA)
            if np.sum([roi_gray]) != 0:
                roi = roi_gray.astype('float')/255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)

                prediction = classifier.predict(roi)[0]

                label = emotion_labels[prediction.argmax()]
                deteksi.append(label)
            else:
                cv2.putText(image[i], 'No Faces', (30, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    return deteksi


def jumlah(deteksi):
    df = pd.DataFrame(deteksi)
    jumlah = pd.value_counts(df[0])

    persen = pd.value_counts(df[0], normalize=True).mul(
        100).round(1).astype(str)+'%'

    return persen


def load_gambar():
    return [cv2.imread(file) for file in glob.glob("images/*")]


def result():
    if not session.get("name"):
        # if not there in the session then redirect to the login page
        return redirect("/masuk")

    ruangan = request.form['ruangan']
    kelas = request.form['kelas']
    mata_kuliah = request.form['mata_kuliah']
    id_dosen = request.form['id_dosen']

    if 'image' not in request.files:
        resp = jsonify({'msg': "No body image attached in request"})
        resp.status_code = 501
        return resp

    image = request.files['image']

    if image.filename == '':
        resp = jsonify({'msg': "No file image selected"})
        resp.status_code = 404
        return resp
    error = {}
    success = False

    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
        success = True
    else:
        error[image.filename] = "File type is not allowed"

    if success and error:
        error['Message'] = "File not uploaded"
        resp = jsonify(error)
        resp.status_code = 500
        return resp
    if success:
        try:
            img = load_gambar()

            deteksi = predict(img)
            output = jumlah(deteksi)
            os.remove(UPLOAD_FOLDER+'/'+filename)

            print('ini deteksi', deteksi)

            biasa = output[0]
            senang = output[1]

            # print(biasa)
            # print(senang)
            # print(ruangan)
            # print(kelas)
            # print(id_dosen)

            newHistori = Histori(
                ruangan, kelas, mata_kuliah, biasa, senang, id_dosen)
            db.session.add(newHistori)
            db.session.commit()

            new = histori_schema.dump(newHistori)
            return redirect("/listdosen")
        except Exception as e:
            resp = {

                'status': 500,
                'msg': "Failed get predict emotion",
                'Error': "Image yang masukan bukan wajah"

            }
            error = jsonify(resp)
            error.status_code = 500
            return error


def getHistoryByDosen(id):
    if not session.get("name"):
        # if not there in the session then redirect to the login page
        return redirect("/masuk")
    print(id)
    konten = Histori.query.filter(Histori.id_dosen == id).all()
    return render_template("riwayat.html", data=enumerate(konten, 1))
