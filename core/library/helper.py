import fitz, hashlib

def ekstrakGambar(location):
   pdf_file = fitz.open(location)
   filenames = []
   for pageNumber, page in enumerate(pdf_file.pages() , start = 1):
      for imgNumber, img in enumerate(page.getImageList(), start=1):
         xref = img[0]

         pix = fitz.Pixmap(pdf_file, xref)

         if pix.n > 4:
            pix = fitz.Pixmap(fitz.csRGB, pix) 

         pix.writePNG(f'imagec_{pageNumber}_{imgNumber}.png') 
         filename = f'imagec_{pageNumber}_{imgNumber}.png'
         filenames.append(filename)
   
   return filenames
         
def hash_file(filename):

   # make a hash object
   h = hashlib.sha1()

   # open file for reading in binary mode
   with open(filename,'rb') as file:

       # loop till the end of the file
       chunk = 0
       while chunk != b'':
           # read only 1024 bytes at a time
           chunk = file.read(1024)
           h.update(chunk)

   # return the hex representation of digest
   return h.hexdigest()


