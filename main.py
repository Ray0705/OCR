import cv2
import preprocessing as P
import segregation as S
import pytesseract
from PIL import Image
import reading_pdf as R

pytesseract.pytesseract.tesseract_cmd =r'C:\Program Files\Tesseract-OCR\tesseract.exe'

test_file_1 = r'Z:\D2K\OCR Code\Task 1\Test\ABFL IGAAP Signed Financials March 2018.pdf'
test_file_2 = r'Z:\D2K\OCR Code\Task 1\Test\Adler Final Signed Financials FY 2018-19 and audit report_.pdf'
test_file_3 = r'Z:\D2K\OCR Code\Task 1\Test\Audit Report ABF_compressed.pdf'
test_file_4 = r'Z:\D2K\OCR Code\Task 1\Test\Financial Statement.pdf'
test_file_5 = r'Z:\D2k\OCR code\Task 1\Test\AK TRADING AUDIT REPORT COMPRESSED.pdf'
test_file_6 = r'Z:\D2k\OCR code\Task 1\Test/Financials AR DR.pdf'
test = test_file_6

conversion_file = r'Z:\D2K\OCR Code\Task 1\Test\conversion_'+ test.split("\\")[-1].split(".")[0]

if R.check_text_or_not(test):
    text = R.read_pdf2(test)
    text_file = open(conversion_file + "\\all.txt", "w", encoding="utf-8")
    text_file.write(text)
    text_file.close()
else:
    # converting the pdf into images
    images = P.convert_into_image(test)
    P.create_new_folder(conversion_file)
    text_file  =  open(conversion_file+"\\all.txt","w",encoding="utf-8")
    for count, image in enumerate(images):
        # saving the image in jpeg or png format as pytessaract requires jpeg file not ppmimage format
        save_img = conversion_file + "\\input_" + str(count + 1) + ".jpg"
        image.save(save_img, "jpeg")
        im = cv2.imread(save_img,0)
        # extracting the data from the images
        img_thresold = P.erosion(im)
        cv2.imwrite(save_img, img_thresold)
        im = Image.open(save_img)
        text= pytesseract.image_to_string(im)
        text_file.write(text)
    text_file.close()

# Separating the data into auditor and annexure report
text_file = open(conversion_file+"\\all.txt","r",encoding="utf-8")
sentences = text_file.readlines()
start_line,stop_line = S.creating_dict(sentences)

if bool(start_line) and bool(stop_line) and len(stop_line) == 2:
    # for auditor report
    start,stop = S.get_start_and_endAR(start_line,stop_line)
    auditor_report = sentences[start:stop+1]
    auditor_file = open(conversion_file+"\\auditor.txt","w")
    for line in auditor_report:
        auditor_file.write(line)
    auditor_file.close()

    # for annexure report
    start_ann,stop_ann = S.get_start_and_endAnn(start_line,stop_line,stop)
    annexure = sentences[start_ann:stop_ann]
    annexure_file = open(conversion_file+"\\annexure.txt","w")
    for line in annexure:
        annexure_file.write(line)
    annexure_file.close()
text_file.close()
