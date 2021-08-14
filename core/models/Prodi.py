from core import db

class Prodi(db.Model):
   id_prodi = db.Column(db.Integer, primary_key = True)
   username = db.Column(db.String(50))
   password = db.Column(db.String(255))
   
   def __init__(self, username, password):
      self.username = username
      self.password = password
      
   @classmethod
   def get_by(cls, input_username):
      return cls.query.filter_by(username=input_username).first()
   