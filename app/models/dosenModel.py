from app import db

class Dosen(db.Model):
    id_dosen = db.Column(db.Integer, primary_key=True)
    nama_dosen = db.Column(db.String(100))
    nipy =db.Column(db.Integer)
    mata_kuliah = db.Column(db.String(200))
    jenis_kelamin = db.Column(db.String(100))

    def __init__(self, nama_dosen, nipy, mata_kuliah, jenis_kelamin):
        self.nama_dosen = nama_dosen
        self.nipy = nipy
        self.mata_kuliah = mata_kuliah
        self.jenis_kelamin = jenis_kelamin