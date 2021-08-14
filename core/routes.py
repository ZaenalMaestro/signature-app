from threading import main_thread
from flask import render_template, request, redirect, flash, session
from flask.helpers import url_for
from werkzeug.utils import secure_filename
from .model import Dosen
from .models.Mahasiswa import *
from .models.Prodi import *
from core import app, db
from .library.helper import (
   ekstrakGambar, get_nilai_hash, hash_file, 
   allowed_file, upload_file, get_id_dosen, hash_password
)
import os

# ================ prodi ================ 
@app.route('/')
def index():
   if not session.get('login'):
      return redirect('/login')
   
   data_dosen = Dosen.query.all()
   return render_template('prodi/dashboard.html', data_dosen = data_dosen)

@app.route('/login', methods=['GET', 'POST'])
def login():
   if session.get('login') == True:
      return redirect('/')
   
   if request.method == 'POST':
      username = request.form['username']
      password = hash_password(request.form['password'])
      data_prodi = Prodi.get_by(username)
      
      if not data_prodi:
         flash('username-invalid')
         return render_template('prodi/login.html', username=username)
         
      if username == data_prodi.username: # cek username
         if password == data_prodi.password: # cek password
            session['login'] = True
            return redirect(url_for('index'))
         else:
            flash('password-invalid')
            return render_template('prodi/login.html', username=username)
      else:
         flash('username-invalid')
         return render_template('prodi/login.html', username=username)
   # REQUEST GET
   return render_template('prodi/login.html')

@app.route('/logout')
def logout():
   session.pop('login')
   return redirect('/login')

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
      file.save(os.path.join('uploads/prodi', filename))
      
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
      input_stambuk = request.form['stambuk']     
      file = request.files['file-skripsi']
      filename = secure_filename(file.filename)
      upload_file('uploads/verifikasi', file)
         
      # # ekstrak gambar dari file pdf
      nama_gambar = ekstrakGambar(os.path.join('uploads/verifikasi', filename))
      daftar_hash = get_nilai_hash(nama_gambar)
      
      # get data mahasiswa by stambuk
      mahasiswa = Mahasiswa.getByStambuk(input_stambuk)
      id_dosen = get_id_dosen(mahasiswa)
      
      hash_dosen = list()
      for id in id_dosen:
         # get data dosen
         row = Dosen.query.filter_by(id_dosen=id).first()
         hash_dosen.append({
            'nama_dosen': row.nama_dosen,
            'tanda_tangan_digital_1': row.tanda_tangan_digital_1,
            'tanda_tangan_digital_2': row.tanda_tangan_digital_2
         })
      
      
      ttd_cocok = 0
      hasil_verifikasi = list()
      for dosen in hash_dosen:
         for mhs in daftar_hash:
            if dosen['tanda_tangan_digital_1'] == mhs or dosen['tanda_tangan_digital_2'] == mhs:
               ttd_cocok += 1
               hasil_verifikasi.append({
                  'nama_dosen':dosen['nama_dosen'],
                  'status': 'valid'
               })
               break
         else:
            hasil_verifikasi.append({
               'nama_dosen':dosen['nama_dosen'],
               'status': 'tidak_valid'
            })
      
      
      hasil_akhir = (ttd_cocok, hasil_verifikasi)
      return render_template('verifikasi/verifikasi.html', hasil_akhir=hasil_akhir)

      
      return 'tanda tangan yang cocok adalah '+ str(ttd_cocok)

   return render_template('verifikasi/verifikasi.html')
