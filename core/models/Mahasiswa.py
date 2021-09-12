from core import db
class Mahasiswa(db.Model):
   stambuk = db.Column(db.String, primary_key = True)
   nama = db.Column(db.String(100))
   pembimbing_1 = db.Column(db.Integer)
   pembimbing_2 = db.Column(db.Integer)
   penguji_1 = db.Column(db.Integer)
   penguji_2 = db.Column(db.Integer)
   penguji_3 = db.Column(db.Integer)
   ketua_sidang = db.Column(db.Integer)
   ketua_prodi = db.Column(db.Integer)
   
   def __init__(
      self, stambuk, nama, pembimbing_1, pembimbing_2, penguji_1, penguji_2, penguji_3, ketua_sidang, ketua_prodi
   ):
      self.stambuk = stambuk
      self.nama = nama
      self.pembimbing_1 = pembimbing_1
      self.pembimbing_2 = pembimbing_2
      self.penguji_1 = penguji_1
      self.penguji_2 = penguji_2
      self.penguji_3 = penguji_3
      self.ketua_sidang = ketua_sidang
      self.ketua_prodi = ketua_prodi
      
   @classmethod
   def getByStambuk(cls, input_stambuk):
      return cls.query.filter_by(stambuk=input_stambuk).first()
   
   @classmethod
   def getAll(cls):
      return cls.query.all()
   
   @classmethod
   def insert(cls, data):
      # # insert data
      my_data = cls(
         data['stambuk'],
         data['nama'],
         data['pembimbing_1'],
         data['pembimbing_2'],
         data['penguji_1'],
         data['penguji_2'],
         data['penguji_3'],
         data['ketua_sidang'],
         data['ketua_prodi'],
      )
      db.session.add(my_data)
      db.session.commit()
   @classmethod
   def update(cls, stambuk, data):
      my_data = cls.query.get(stambuk)
      
      my_data.stambuk = data['stambuk']
      my_data.nama = data['nama']
      my_data.pembimbing_1 =data['pembimbing_1']
      my_data.pembimbing_2 =data['pembimbing_2']
      my_data.penguji_1 =data['penguji_1']
      my_data.penguji_2 =data['penguji_2']
      my_data.penguji_3 =data['penguji_3']
      my_data.ketua_sidang =data['ketua_sidang']
      my_data.ketua_prodi =data['ketua_prodi']
      
      db.session.commit()
      
   @classmethod
   def delete(cls, stambuk):
      my_data = cls.query.get(stambuk)
      db.session.delete(my_data)
      db.session.commit()