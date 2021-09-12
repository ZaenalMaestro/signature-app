p = 59
q = 67

n = p * q
tautient_n = (p-1) * (q-1)
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
         
def faktor_pembagi_bilangan(e):
   hasil = set()
   for i in range(1, (e+1)):
      if e % i == 0:
         hasil.add(i)
   return hasil

def relatif_prima(a, b):
   # fpb = faktor persekutuan bersama
   fpb = faktor_pembagi_bilangan(a).intersection(faktor_pembagi_bilangan(b))
   fpb = list(fpb)
   
   # jika fpb == 1 maka True
   # jika fpb != 1 maka False
   return True if len(fpb) == 1 and fpb[0] == 1 else False

def generate_e(tautient_n):
   for e in range(3, tautient_n):
      if relatif_prima(tautient_n, e):
         return e
      
def generate_d(tautient_n, e):
   k_value = 1
   hasil_akhir = 0
   while True:
      hasil = (1 + (k_value * tautient_n)) / e
      if cek_bilangan_bulat(hasil):
         hasil_akhir = hasil
         break
      k_value +=1
   return int(hasil_akhir)


def enkripsi(plaintext):
   # private key (d, n)
   global tautient_n, n
   e = generate_e(tautient_n)
   d = generate_d(tautient_n, e)
   
   # convert plaintext ke ASCII
   nilai_ascii = []
   for karakter in plaintext:
      nilai_ascii.append(ord(karakter))
   
   # enkripsi
   chipertext = []
   for nilai in nilai_ascii:
      enkripsi = (nilai**d) % n
      chipertext.append(enkripsi)
   return tuple(chipertext)

def dekripsi(chipertext):
   # public key (e, n)
   global tautient_n, n
   # nilai dekripsi
   e = generate_e(tautient_n)
   plaintext = []
   
   for chiper in chipertext:
      dekripsi_chipertext = (chiper**e) % n
      plaintext.append(dekripsi_chipertext)
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
