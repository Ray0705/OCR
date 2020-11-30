# OCR
Optical Character Recognition

### Main.py 
In this file all the main code is present.

### Preprocessing.py 
This contains all the preprocessing function which are required in the main OCR.
Packages used - numpy, PIL, pdf2image,os,shutil,cv2.
functions - 
+ Create new folder
+ convert into images - converting the one pdf into one image which will be used as input in the OCR(packages used pdf2image.convert_from_path
+ erosion 
+ thresolding

### Reading_pdf.py
to directly read the data if the pdf is non- scanned file
packages used - tika, subprocess
functions- 
+ reading file through tika -  Tika is used to extract the text data from the non scanned data.
+ checking whether the pdf is scanned or non-scanned pdf

### segragation.py 
Trying to create 2 document in which one will be auditor report and another will be annexure 
packages used - itertools
functions - 
+ creating dict - to store the indexes and words of the start word and the end word
+ get_start_and_endAR -  to get the start and end indexes of the auditor report
+ get_start_and_endAnn -  to get the start and end indexes of the annexure

### deskew.py
This is to untitled the page which are getting tilted during the scanning or any other reason.
packages used - opencv, numpy, PIL, scipy
functions - 
+ correct_skew - to correct the orientation of the page automatically

