from core import db


class Dosen(db.Model):
   id_dosen = db.Column(db.Integer, primary_key = True)
   nama_dosen = db.Column(db.String(100))
   tanda_tangan_digital_1 = db.Column(db.String(100))
   tanda_tangan_digital_2 = db.Column(db.String(100))
   
   def __init__(self, nama_dosen, tanda_tangan_digital_1, tanda_tangan_digital_2):
      self.nama_dosen = nama_dosen
      self.tanda_tangan_digital_1 = tanda_tangan_digital_1
      self.tanda_tangan_digital_2 = tanda_tangan_digital_2