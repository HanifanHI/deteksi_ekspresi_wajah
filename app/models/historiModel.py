from datetime import datetime
from app import db


class Histori(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ruangan = db.Column(db.String(100))
    kelas = db.Column(db.String(100))
    mata_kuliah = db.Column(db.String(100))
    tanggal = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    hasilSenang = db.Column(db.String(100))
    hasilBiasa = db.Column(db.String(100))
    id_dosen = db.Column(db.VARCHAR(4))

    def __init__(self, ruangan, kelas, mata_kuliah, hasilSenang, hasilBiasa, id_dosen):
        self.ruangan = ruangan
        self.kelas = kelas
        self.mata_kuliah = mata_kuliah
        self.hasilSenang = hasilSenang
        self.hasilBiasa = hasilBiasa
        self.id_dosen = id_dosen