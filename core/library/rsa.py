p = 59
q = 67

n = p * q
tau_n = (p-1) * (q-1)

def cek_bilangan_bulat(bilangan):
   bilangan = float(bilangan)
   bilangan = str(bilangan)
   
   # cek bilangan negatif
   for i in bilangan:
      if i == '-':
         return False
   
   # cek bilangan pecahan
   angka = bilangan.split('.')   
   for i in angka[1]:
      return False if int(i) != 0 else True
         
def faktor_bilangan(e):
   faktor_bilangan = set()
   for i in range(1, (e+1)):
      if e % i == 0:
         faktor_bilangan.add(i)
   return faktor_bilangan

def relatif_prima(a, b):
   # fpb = faktor persekutuan terbesar
   fpb = faktor_bilangan(a).intersection(faktor_bilangan(b))
   fpb = list(fpb)
   
   # jika fpb == 1 relatif prima else tidak relatif prima
   return True if len(fpb) == 1 and fpb[0] == 1 else False

def generate_e(tau_n):
   for e in range(3, tau_n):
      if relatif_prima(tau_n, e):
         return e
      
def generate_d(tau_n, e):
   k_value = 1
   hasil_akhir = 0
   while True:
      hasil = (1 + (k_value * tau_n)) / e
      if cek_bilangan_bulat(hasil):
         hasil_akhir = hasil
         break
      k_value +=1
   return int(hasil_akhir)


def enkripsi(plaintext):
   global tau_n, n
   # kunci enkripsi
   kunci_enkripsi = generate_e(tau_n)
   
   # convert plaintext ke ASCII
   nilai_ascii = []
   for karakter in plaintext:
      nilai_ascii.append(ord(karakter))
   
   # enkripsi
   chipertext = []
   for nilai in nilai_ascii:
      enkripsi = (nilai**kunci_enkripsi) % n
      chipertext.append(enkripsi)
   return tuple(chipertext)

def dekripsi(chipertext):
   global tau_n, n
   # nilai dekripsi
   kunci_dekripsi = generate_d(tau_n, generate_e(tau_n))
   plaintext = []
   
   for chiper in chipertext:
      enkripsi = (chiper**kunci_dekripsi) % n
      plaintext.append(enkripsi)
   teks = ''.join(map(chr, plaintext))
   return teks

def chipertext_to_str(chipertext):
   teks = ''
   for index, chiper in enumerate(chipertext):
      if index == 0:
         teks += str(chiper)
      else:
         teks += ',' + str(chiper)
   return teks

def str_to_chipertext(string_value):
   string_value = string_value.split(',')
   chipertext = []
   for string in string_value:
      chipertext.append(int(string))
   return tuple(chipertext)
