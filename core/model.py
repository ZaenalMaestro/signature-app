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
      
   @classmethod
   def insert(cls, nama_dosen, daftar_hash):
      data = cls(nama_dosen, daftar_hash[0], daftar_hash[1])
      db.session.add(data)
      db.session.commit()
      
   @classmethod
   def update(cls, id_dosen, nama_dosen, daftar_hash):
      data = cls.query.get(id_dosen)
      data.nama_dosen = nama_dosen
      data.tanda_tangan_digital_1 = daftar_hash[0]
      data.tanda_tangan_digital_2 = daftar_hash[1]
      db.session.commit()
      
