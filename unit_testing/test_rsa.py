import sys
sys.path.append('../')
from core.library.rsa import *

def test_bilangan_bulat():
   bilangan_bulat = [1, 2, 3, 4]
   for bilangan in bilangan_bulat:
      assert cek_bilangan_bulat(bilangan) == True
      
def test_enkripsi():
   hasil_enkripsi = (2338, 1887, 900, 2651, 2214, 2214, 2651, 317, 2, 3376, 1030, 191, 2651, 1627)
   assert enkripsi('Muhammad Akbar') == hasil_enkripsi