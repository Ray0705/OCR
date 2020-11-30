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

