from app import app
from flask import request, jsonify, render_template, session, redirect
from flask_marshmallow import Marshmallow
from app.models.dosenModel import db, Dosen

ma = Marshmallow(app)


class DosenSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nama_dosen', 'nipy', 'mata_kuliah', 'jenis_kelamin')


# init schema
dosenSchema = DosenSchema()
dosensSchema = DosenSchema(many=True)



def createDosen():
    nama_dosen = request.form['nama_dosen']
    nipy = request.form['nipy']
    mata_kuliah = request.form['mata_kuliah']
    jenis_kelamin = request.form['jenis_kelamin']
    

    newsDosen = Dosen(nama_dosen=nama_dosen, nipy=nipy, mata_kuliah=mata_kuliah, jenis_kelamin=jenis_kelamin)

    db.session.add(newsDosen)
    db.session.commit()
    new = dosenSchema.dump(newsDosen)
    return jsonify({"msg": "success get all dosen", "status": 200, "data": new})


def getAlldosenHistori():
    if not session.get("name"):
        # if not there in the session then redirect to the login page
        return redirect("/masuk")
    allDosen = Dosen.query.all()
    return render_template('listdosen.html', data=enumerate(allDosen, 1))

def getAllDosenPredik():
    allDosen = Dosen.query.all()
    return render_template('predik.html', data=enumerate(allDosen, 1))

def getDosenById(id):
    dosen = Dosen.query.get(id)
    dosenDetails = dosenSchema.dump(dosen)
    return jsonify({"msg": "Success get mitra by id", "status": 200, "data": dosenDetails})


def updateDosen(id):
    dosen = Dosen.query.get(id)
    nama_dosen = request.form['nama_dosen']
    mata_kuliah = request.form['mata_kuliah']

    dosen.nama_dosen = nama_dosen
    dosen.mata_kuliah = mata_kuliah

    db.session.commit()
    dosenUpdate = dosenSchema.dump(dosen)
    return jsonify({"msg": "Success update dosen", "status": 200, "data": dosenUpdate})


def deleteDosen(id):
    dosen = Dosen.query.get(id)
    db.session.delete(dosen)
    db.session.commit()
    dosenDelete = dosenSchema.dump(dosen)
    return jsonify({"msg": "Success Delete dosen", "status": 200, "data": dosenDelete})
