import cv2
import numpy as np
from PIL import Image
from scipy.ndimage import interpolation as inter


def correct_skew(image_file,delta = 1,limit = 5):
    """input as image file and output as numpy array"""
    """Projection profile method"""
    img = Image.open(image_file)
    # convert to binary
    wd, ht = img.size
    pix = np.array(img.convert('1').getdata(), np.uint8)
    bin_img = 1 - (pix.reshape((ht, wd)) / 255.0)


    def find_score(arr, angle):
        data = inter.rotate(arr, angle, reshape=False, order=0)
        histogram = np.sum(data, axis=1)
        score = np.sum((histogram[1:] - hist[:-1]) ** 2)
        return histogram, score

    angles = np.arange(-limit, limit+delta, delta)
    scores = []
    for angle in angles:
        hist, score = find_score(bin_img, angle)
        scores.append(score)

    # calculating the best angle
    best_score = max(scores)
    best_angle = angles[scores.index(best_score)]

    # correct skew
    data = inter.rotate(bin_img, best_angle, reshape=False, order=0)
    image = Image.fromarray((255 * data).astype("uint8")).convert("RGB")
    rotate_img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)# this will give you black background with white text
    rotated_image = ~rotate_img # to make it white background and blacke text we use ~ sign
    return rotated_image

# for example
# img = r"Z:\D2K\OCR code\Task 1\Test\result\input_2_tilted.jpg"
# rotated_img = correct_skew(img)
# cv2.imshow("rotated_img",rotated_img)

