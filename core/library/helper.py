from werkzeug.utils import secure_filename
import fitz, hashlib
import os

def ekstrakGambar(location):
   pdf_file = fitz.open(location)
   filenames = []
   for pageNumber, page in enumerate(pdf_file.pages() , start = 1):
      for imgNumber, img in enumerate(page.getImageList(), start=1):
         xref = img[0]

         pix = fitz.Pixmap(pdf_file, xref)

         if pix.n > 4:
            pix = fitz.Pixmap(fitz.csRGB, pix) 

         filename = f'image_{pageNumber}_{imgNumber}.png'
         pix.writePNG(filename) 
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

def allowed_file(filename):
   ALLOWED_EXTENSION = set(['pdf'])
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION

def upload_file(path, file):
   filename = secure_filename(file.filename)
   
   if file and allowed_file(filename):
      filename = secure_filename(filename)
      file.save(os.path.join(path, filename))


