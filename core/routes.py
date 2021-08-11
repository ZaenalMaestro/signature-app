from threading import main_thread
from flask import render_template, request, redirect, flash
from flask.helpers import url_for
from werkzeug.utils import secure_filename
from .model import Dosen, Mahasiswa
from core import app, db
from .library.helper import ekstrakGambar, hash_file, allowed_file, upload_file
import os

from pprint import pprint

# ================ prodi ================ 
@app.route('/')
def index():
   data_dosen = Dosen.query.all()
   return render_template('prodi/dashboard.html', data_dosen = data_dosen)

@app.route('/login')
def login():
   return render_template('prodi/login.html')

# upload gambar
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
      nama_gambar = ekstrakGambar(os.path.join('uploads/prodi', filename))
      
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


@app.route('/verifikasi', methods=['GET', 'POST'])
def verifikasi():
   if request.method == 'POST':
      stambuk = request.form['stambuk']     
      file = request.files['file-skripsi']
      filename = secure_filename(file.filename)
      upload_file('uploads/verifikasi', file)
         
      # ekstrak gambar dari file pdf
      nama_gambar = ekstrakGambar(os.path.join('uploads/verifikasi', filename))
      daftar_hash = []
      for gambar in nama_gambar:
         daftar_hash.append(hash_file(gambar))
         os.remove(gambar)
      
      # get data mahasiswa by stambuk
      
      # get data dosen
      row = Dosen.query.filter_by(id_dosen=2).first()
      hash_dosen = list()
      hash_dosen.append({
         'nama_dosen': row.nama_dosen,
         'tanda_tangan_digital_1': row.tanda_tangan_digital_1,
         'tanda_tangan_digital_2': row.tanda_tangan_digital_2
      })
      ttd_cocok = 0
      for dosen in hash_dosen:
         for mhs in daftar_hash:
            if dosen['tanda_tangan_digital_1'] == mhs or dosen['tanda_tangan_digital_2'] == mhs:
               ttd_cocok += 1
      
      return 'tanda tangan yang cocok adalah '+ str(ttd_cocok)
   rows = Mahasiswa.query.filter_by(stambuk='13020160099').first()
   return render_template('verifikasi/verifikasi.html',rows=rows)
