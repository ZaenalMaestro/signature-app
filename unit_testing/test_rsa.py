import sys
sys.path.append('../')
from core.library.rsa import *

def test_bilangan_bulat():
      assert cek_bilangan_bulat(120) == True
      assert cek_bilangan_bulat(-120) == False
      assert cek_bilangan_bulat(31.22) == False
      
def test_faktor_bilangan():
   assert faktor_pembagi_bilangan(2) == {1, 2}
   assert faktor_pembagi_bilangan(24) == {1, 2, 3, 4, 6, 8, 12, 24}
   assert faktor_pembagi_bilangan(32) == {1, 2, 4, 8, 16, 32}
   
def test_relatif_prima():
   assert relatif_prima(11, 7) == True
   assert relatif_prima(27, 15) == False
   
def test_generate_e():
   assert generate_e(tautient_n) == 5
   
def test_generate_d():
   e = generate_e(tautient_n)
   assert generate_d(tautient_n, 5) == 2297
   
def test_enkripsi():
   hasil_enkripsi = (2338, 1887, 900, 2651, 2214, 2214, 2651, 317, 2, 3376, 1030, 191, 2651, 1627)
   assert enkripsi('Muhammad Akbar') == hasil_enkripsi
   
def test_dekripsi():
   hasil_enkripsi = (2338, 1887, 900, 2651, 2214, 2214, 2651, 317, 2, 3376, 1030, 191, 2651, 1627)
   assert dekripsi(hasil_enkripsi) == 'Muhammad Akbar'
   
def test_chipertext_to_str():
   chipertext = enkripsi('Muhammad Akbar')
   nilai_string = '2338,1887,900,2651,2214,2214,2651,317,2,3376,1030,191,2651,1627'
   assert chipertext_to_str(chipertext) == nilai_string

def test_str_to_chipertext():
   nilai_string = '2338,1887,900,2651,2214,2214,2651,317,2,3376,1030,191,2651,1627'
   chipertext = (2338, 1887, 900, 2651, 2214, 2214, 2651, 317, 2, 3376, 1030, 191, 2651, 1627)
   assert str_to_chipertext(nilai_string) == chipertext
   

   
