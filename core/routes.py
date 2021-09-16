from flask import render_template, request, redirect, flash, session
from flask.helpers import url_for
from werkzeug.utils import secure_filename
from .models.Dosen import *
from .models.Mahasiswa import *
from .models.Prodi import *
from core import app, db
from .library.helper import (
   ekstrakGambar, get_nilai_hash, hash_file, 
   allowed_file, upload_file, get_id_dosen, hash_password
)
from .library.rsa import chipertext_to_str, enkripsi, dekripsi, str_to_chipertext
import os

# ================ prodi ================ 
@app.route('/')
def index():
   if not session.get('login'):
      return redirect('/login')
   
   data = {
      'dosen': Dosen.query.all(),
      'active_link': 'dashboard'
   }
   return render_template('prodi/dashboard.html', data = data)

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
   split_file = filename.split('.')
   nama_dosen = request.form['nama-dosen']   
   
   if 'file' not in request.files or filename == '':
      return redirect(url_for('index'))
   
   if file and allowed_file(filename):
      filename = secure_filename(filename)
      path = os.path.join('uploads/prodi', filename)
      file.save(path)
      
      # ekstrak gambar dari file pdf
      nama_gambar = ekstrakGambar(path)
      # hapus file 
      os.remove(path)
      # get nilai hash semua gambar
      daftar_hash = get_nilai_hash(nama_gambar)
      data = []
      for nilai_hash in daftar_hash:
         chipertext = enkripsi(nilai_hash)
         data.append(chipertext_to_str(chipertext))
         
   # # insert data
   Dosen.insert(nama_dosen, data)
   # set flash
   flash('Tanda Tangan digital berhasil dibuat')      
   return redirect(url_for('index'))

# update ttd digital
# upload gambar
@app.route('/update_upload', methods=['POST'])
def update_ttd_digital():
   # get request
   file = request.files['file-update']
   filename = secure_filename(file.filename)
   id_dosen = request.form['id-dosen']
   nama_dosen = request.form['nama-dosen']
   
   if file and allowed_file(filename):
      filename = secure_filename(filename)
      path = os.path.join('uploads/prodi', filename)
      file.save(path)
      
      # ekstrak gambar dari file pdf
      nama_gambar = ekstrakGambar(path)
      # hapus file setelah ekstrak gambar
      os.remove(path)
      # get nilai hash semua gambar
      daftar_hash = get_nilai_hash(nama_gambar)
      data = []
      for nilai_hash in daftar_hash:
         chipertext = enkripsi(nilai_hash)
         data.append(chipertext_to_str(chipertext))
   else:
      data = [request.form['hash-1'], request.form['hash-2']]
   
   # update data
   Dosen.update(id_dosen, nama_dosen, data)
   # set flash
   flash('Data berhasil diubah')  
   return redirect(url_for('index'))

# menu mahasiswa
@app.route('/mahasiswa')
def show_mahasiswa():
   if not session.get('login'):
      return redirect('/login')
   
   data = {
      'mahasiswa': Mahasiswa.getAll(),
      'dosen': Dosen.query.all(),
      'active_link': 'mahasiswa'
   }
   
   return render_template('prodi/mahasiswa.html', data = data)

# menu mahasiswa - tambah data
@app.route('/addmahasiswa', methods=['POST'])
def tambah_mahasiswa():
   data_input = {
      'stambuk': request.form['stambuk'],
      'nama': request.form['nama'],
      'pembimbing_1': request.form['pembimbing-1'],
      'pembimbing_2': request.form['pembimbing-2'],
      'penguji_1': request.form['penguji-1'],
      'penguji_2': request.form['penguji-2'],
      'penguji_3': request.form['penguji-3'],
      'ketua_sidang': request.form['ketua-sidang'],
      'ketua_prodi': request.form['ketua-prodi'],
      'dekan': request.form['dekan']
   }
   
   mahasiswa = Mahasiswa.getByStambuk(data_input['stambuk'])
   if not mahasiswa: # tambah data jika stambuk belum terdaftar
      Mahasiswa.insert(data_input)
      flash('data mahasiswa berhasil ditambahkan')
      return redirect('/mahasiswa')
   else:
      flash('error')
      return redirect('/mahasiswa')
   
# update mahasiswa
@app.route('/updatemahasiswa', methods=['POST'])
def update_mahasiswa():
   if request.form['old-stambuk'] != request.form['stambuk']:
      row = Mahasiswa.getByStambuk(request.form['stambuk'])
      if row:
         flash('error')
         return redirect('/mahasiswa')
      
   data_input = {
      'stambuk': request.form['stambuk'],
      'nama': request.form['nama'],
      'pembimbing_1': request.form['pembimbing-1'],
      'pembimbing_2': request.form['pembimbing-2'],
      'penguji_1': request.form['penguji-1'],
      'penguji_2': request.form['penguji-2'],
      'penguji_3': request.form['penguji-3'],
      'ketua_sidang': request.form['ketua-sidang'],
      'ketua_prodi': request.form['ketua-prodi'],
      'dekan': request.form['dekan'],
   }

   Mahasiswa.update(request.form['old-stambuk'], data_input)
   flash('data mahasiswa berhasil diubah')
   return redirect('/mahasiswa')
   
# hapus mahasiswa
@app.route('/hapusmahasiswa', methods=['POST'])
def hapus_mahasiswa():
   Mahasiswa.delete(request.form['stambuk'])
   flash('data mahasiswa berhasil dihapus')
   return redirect('/mahasiswa')



# ================ verifikasi, mahasiswa ================ 
@app.route('/verifikasi', methods=['GET', 'POST'])
def verifikasi():
   if request.method == 'POST':
      input_stambuk = request.form['stambuk']     
      file = request.files['file-skripsi']
      filename = secure_filename(file.filename)
      nama_file, extension = filename.split('.')
      
      if extension != 'pdf':
         flash('invalid_extension')
         return render_template('verifikasi/verifikasi.html', stambuk=input_stambuk)
      
      path = os.path.join('uploads/verifikasi', filename)
      upload_file('uploads/verifikasi', file)
         
      # # ekstrak gambar dari file pdf
      nama_gambar = ekstrakGambar(path)
      daftar_hash = get_nilai_hash(nama_gambar)
      # hapus file 
      os.remove(path)
      
      # get data mahasiswa by stambuk
      mahasiswa = Mahasiswa.getByStambuk(input_stambuk)
      if not mahasiswa:
         flash('stambuk_invalid')
         return render_template('verifikasi/verifikasi.html', stambuk=input_stambuk)
      
      id_dosen = get_id_dosen(mahasiswa)      
      hash_dosen = list()
      for id in id_dosen:
         # get data dosen
         row = Dosen.query.filter_by(id_dosen=id).first()
         # dekripsi
         tanda_tangan_digital_1 = str_to_chipertext(row.tanda_tangan_digital_1)
         tanda_tangan_digital_2 = str_to_chipertext(row.tanda_tangan_digital_2)
         hash_dosen.append({
            'nama_dosen': row.nama_dosen,
            'hash_1': dekripsi(tanda_tangan_digital_1),
            'hash_2': dekripsi(tanda_tangan_digital_2)
         })
      
      
      hasil_verifikasi = list()
      jabatan_dosen = ['Pembimbing Utama', 'Pembimbing Pendamping', 'Penguji 1',  
                        'Penguji 2', 'Penguji 3', 'Ketua Sidang', 'Ketua Prodi', 'Dekan']
      for dosen, jabatan in zip(hash_dosen, jabatan_dosen):
         for mhs in daftar_hash:
            if dosen['hash_1'] == mhs or dosen['hash_2'] == mhs:
               hasil_verifikasi.append({
                  'nama_dosen':dosen['nama_dosen'],
                  'jabatan': jabatan,
                  'status': 'valid'
               })
               break
         else:
            hasil_verifikasi.append({
               'nama_dosen':dosen['nama_dosen'],
               'jabatan': jabatan,
               'status': 'tidak_valid'
            })
      
      # return str(hasil_verifikasi)
      return render_template('verifikasi/verifikasi.html', hasil_akhir=hasil_verifikasi)

   return render_template('verifikasi/verifikasi.html')
