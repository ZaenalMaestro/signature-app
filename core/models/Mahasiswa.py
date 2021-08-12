from core import db
class Mahasiswa(db.Model):
   stambuk = db.Column(db.String, primary_key = True)
   nama = db.Column(db.String(100))
   pembimbing_1 = db.Column(db.Integer)
   pembimbing_2 = db.Column(db.Integer)
   penguji_1 = db.Column(db.Integer)
   penguji_2 = db.Column(db.Integer)
   penguji_3 = db.Column(db.Integer)
   ketua_prodi = db.Column(db.Integer)
   
   def __init__(
      self, stambuk, nama, pembimbing_1, pembimbing_2, penguji_1, penguji_2, penguji_3, ketua_prodi
   ):
      self.stambuk = stambuk
      self.nama = nama
      self.pembimbing_1 = pembimbing_1
      self.pembimbing_2 = pembimbing_2
      self.penguji_1 = penguji_1
      self.penguji_2 = penguji_2
      self.penguji_3 = penguji_3
      self.ketua_prodi = ketua_prodi
      
   @classmethod
   def getByStambuk(cls, input_stambuk):
      return cls.query.filter_by(stambuk=input_stambuk).first()