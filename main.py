import cv2
import preprocessing as P
import segregation as S
import pytesseract
from PIL import Image
import reading_pdf as R
from PyPDF2 import PdfFileReader
from tika import parser
pytesseract.pytesseract.tesseract_cmd =r'C:\Program Files\Tesseract-OCR\tesseract.exe'
test_file_1 = r'Z:\D2K\OCR Code\Task 1\Test\ABFL IGAAP Signed Financials March 2018.pdf'
test_file_2 = r'Z:\D2K\OCR Code\Task 1\Test\Adler Final Signed Financials FY 2018-19 and audit report_.pdf'
test_file_3 = r'Z:\D2K\OCR Code\Task 1\Test\Audit Report ABF_compressed.pdf'
test_file_4 = r'Z:\D2K\OCR Code\Task 1\Test\Financial Statement.pdf'
test_file_5 = r'Z:\D2k\OCR code\Task 1\Test\AK TRADING AUDIT REPORT COMPRESSED.pdf'
test_file_6 = r'Z:\D2k\OCR code\Task 1\Test/Financials AR DR.pdf'
test_file = test_file_2

# Creating the path or folder where the pdf is converted to text file, the folder name is converted the filename
# for eg:- if the name of the pdf file is financials.pdf then the created folder will have converted_financials
converted_folder = r'Z:\D2K\OCR Code\Task 1\Test'+'\\'+ test_file.split("\\")[-1].split(".")[0]


#   if it is not scanned then it will go through if condition or it will run the else condition. as the in the function we are finding whether the given file is 
#   scanned or not 
if not R.check_scanned_or_not(test_file):
    P.create_new_folder(converted_folder)
    text_file = converted_folder + "\\" + test_file.split("\\")[-1].split(".")[0] + ".txt"
    text_file = open(text_file,"w",encoding="utf-8")
    text = R.read_pdf(test_file)
    text_file.write(text)
    text_file.close()
else:
    # converting the pdf into images
    images = P.convert_into_image(test_file)
    P.create_new_folder(converted_folder)
    text_file  =  open(converted_folder + "\\" + test_file.split("\\")[-1].split(".")[0] +".txt","w",encoding="utf-8")
    for count, image in enumerate(images):
        # saving the image in jpeg or png format as pytessaract requires jpeg file not ppmimage format
        # saving the image in the converted folder
        save_img = converted_folder + "\\input_" + str(count + 1) + ".jpg"
        image.save(save_img, "jpeg")
        im = cv2.imread(save_img,0)
        # extracting the data from the images
        im_erode = P.erosion(im)
        im_dilate = P.dialtion(im_erode)
        # this is for viewing the image and store it in the same folder but we are overwrite the image where previous image.
        cv2.imwrite(save_img, im_dilate)
        # im = Image.open(save_img)
        text = pytesseract.image_to_string(im_dilate)
        text_file.write(text)
    text_file.close()

# Separating the data into auditor and annexure report
# saving the txt file with the same name as pdf
text_file = open(converted_folder + "\\" + test_file.split("\\")[-1].split(".")[0] +".txt","r",encoding="utf-8")
sentences = text_file.readlines()
# creating the dictionary to start and stop line for auditor and annexure report
start_line,stop_line = S.creating_dict(sentences)

if bool(start_line) and bool(stop_line) and len(stop_line) == 2:
    # for auditor report
    start,stop = S.get_start_and_endAR(start_line,stop_line)
    auditor_report = sentences[start:stop+1]
    auditor_file = open(converted_folder+"\\auditor_report.txt","w")
    for line in auditor_report:
        auditor_file.write(line)
    auditor_file.close()

    # for annexure report
    start_ann,stop_ann = S.get_start_and_endAnn(start_line,stop_line,stop)
    annexure = sentences[start_ann:stop_ann]
    annexure_file = open(converted_folder+"\\annexure_part.txt","w")
    for line in annexure:
        annexure_file.write(line)
    annexure_file.close()
text_file.close()
