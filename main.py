import cv2
import preprocessing as P
import segregation as S
import pytesseract
import deskew
import reading_pdf as R

pytesseract.pytesseract.tesseract_cmd =r'C:\Program Files\Tesseract-OCR\tesseract.exe'
test_file_1 = r'Test\ABFL IGAAP Signed Financials March 2018.pdf'
test_file = test_file_1

# Creating the path or folder where the pdf is converted to text file, the folder name is converted the filename
# for eg:- if the name of the pdf file is financials.pdf then the created folder will have converted_financials
converted_folder = r'Test'+'\\'+ test_file.split("\\")[-1].split(".")[0]


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
    text_file = open(converted_folder + "\\" + test_file.split("\\")[-1].split(".")[0] +".txt","w",encoding="utf-8")
    for count, image in enumerate(images):
        # saving the image in jpeg or png format as pytessaract requires jpeg file not ppmimage format
        # saving the image in the converted folder
        save_img = converted_folder + "\\input_" + str(count + 1) + ".jpg"
        image.save(save_img, "jpeg")
        # trying to rotate the image if tilted
        image = deskew.correct_skew(save_img)
        # converting it into gray scale
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        # extracting the data from the images
        im_erode = P.erosion(gray)
        im_dilate = P.dialtion(im_erode)
        # this is for viewing the image and store it in the same folder but we are overwrite the image where previous image.
        cv2.imwrite(save_img, im_dilate)
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
