import numpy as np
from PIL import ImageEnhance
from pdf2image import convert_from_path
import os
import shutil
from enchant.checker import SpellChecker
import cv2


# converting the pdf to images for OCR

def create_new_folder(conversion_file):
    if os.path.isdir(conversion_file):
        shutil.rmtree(conversion_file, ignore_errors=True)
    os.mkdir(conversion_file)


def convert_into_image(test_file,dpi=300):
    images = convert_from_path(test_file, dpi)
    return images

def dialtion(image):
    kernel = np.ones((5, 5))
    imgDial = cv2.dilate(image, kernel, iterations=2)  # APPLY DILATION
    imgDial

def erosion(image):
    kernel = np.ones((5, 5))
    imgThreshold = cv2.erode(image, kernel, iterations=1)  # APPLY EROSION it removes the smallest of noise
    return imgThreshold

def canny_edge(image):
    edges = cv2.Canny(image,150,255)
    return edges

def contrast(im,level = 1):
    enchancer = ImageEnhance.Contrast(im)
    return enchancer.enhance(level)

def thresolding(image):
    # return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

def spellchecker(sentence):
    spell = SpellChecker()
    misspelled = spell.unknown(sentence.split())
    dict_ = {word: spell.correction(word) for word in misspelled}
    for word, c_word in dict_.items():
        sentence = sentence.replace(word, c_word)

def print_some(text):
    text = str(text)
    print(text)

def correcting_image(image):
    # import the necessary packages
    import numpy as np
    import cv2


    # load the image from disk
    image = cv2.imread(image)

    # convert the image to grayscale and flip the foreground
    # and background to ensure foreground is now "white" and
    # the background is "black"
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)

    # threshold the image, setting all foreground pixels to
    # 255 and all background pixels to 0
    thresh = cv2.threshold(gray, 0, 255,
                           cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # grab the (x, y) coordinates of all pixel values that
    # are greater than zero, then use these coordinates to
    # compute a rotated bounding box that contains all
    # coordinates
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]

    # the `cv2.minAreaRect` function returns values in the
    # range [-90, 0); as the rectangle rotates clockwise the
    # returned angle trends to 0 -- in this special case we
    # need to add 90 degrees to the angle
    if angle < -45:
        angle = -(90 + angle)

    # otherwise, just take the inverse of the angle to make
    # it positive
    else:
        angle = -angle

    # rotate the image to deskew it
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h),
                             flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    cv2.putText(rotated, "Angle: {:.2f} degrees".format(angle),
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    return rotated
