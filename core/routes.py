from flask import render_template, request, redirect, flash
from flask.helpers import url_for
from werkzeug.utils import secure_filename
from .model import Dosen
from core import app, db
from .library.helper import ekstrakGambar, hash_file
import os

# ================ prodi ================ 
@app.route('/')
def index():
   data_dosen = Dosen.query.all()
   return render_template('prodi/dashboard.html', data_dosen = data_dosen)

@app.route('/login')
def login():
   return render_template('prodi/login.html')

# upload gambar
def allowed_file(filename):
   ALLOWED_EXTENSION = set(['pdf'])
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION

@app.route('/upload', methods=['POST'])
def upload():
   # get request
   file = request.files['file']
   filename = secure_filename(file.filename)
   nama_dosen = request.form['nama-dosen']
      
   
   if 'file' not in request.files or filename == '':
      return redirect(url_for('index'))
   
   if file and allowed_file(filename):
      filename = secure_filename(filename)
      file.save(os.path.join('uploads', filename))
      
      # ekstrak gambar dari file pdf
      nama_gambar = ekstrakGambar(os.path.join('uploads', filename))
      
      daftar_hash = []
      for gambar in nama_gambar:
         daftar_hash.append(hash_file(gambar))
         os.remove(gambar)
      
      

   # # insert data
   my_data = Dosen(nama_dosen, daftar_hash[0], daftar_hash[1])
   db.session.add(my_data)
   db.session.commit()
   
   # set flash
   flash('Tanda Tangan digital berhasil dibuat')
      
   return redirect(url_for('index'))


# ================ verifikasi, mahasiswa ================ 
@app.route('/verifikasi')
def verifikasi():
   return render_template('verifikasi/verifikasi.html')
