"""
Made by: Ryken Santillan
Version Started: 2022-12-27
Version Finished: 2022-12-28
Class: ImageReader
Description:
      - This class returns an array of the image's information
"""

import numpy as np
import cv2
import pytesseract
from imutils import contours

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\saen7\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'


def processImage(imageFile):
    # Reading and Processing the Image
    board = cv2.imread(imageFile)
    gray = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY)
    thr = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 57, 5)

    # Obtaining Box Contours
    conts = cv2.findContours(thr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    conts = conts[0] if len(conts) == 2 else conts[1]
    for i in conts:
        area = cv2.contourArea(i)
        if area < 5000:  # Box
            cv2.drawContours(thr, [i], -1, (0, 0, 0), -1)

    # Morphing Hori/Verti Lines
    vertLines = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 5))
    thr = cv2.morphologyEx(thr, cv2.MORPH_CLOSE, vertLines, iterations=9)
    horiLines = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 1))
    thr = cv2.morphologyEx(thr, cv2.MORPH_CLOSE, horiLines, iterations=4)

    # Sorting via 2D Array Format
        # Top To Bottom
    reverse = 255 - thr
    conts = cv2.findContours(reverse, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    conts = conts[0] if len(conts) == 2 else conts[1]
    conts, _ = contours.sort_contours(conts, method="top-to-bottom") #

    # Top To Bottom
    magicSq_rows, row = [], []
    for (i, j) in enumerate(conts, 1):
        area = cv2.contourArea(j)
        if area < 20000:
            row.append(j)
            if i % 3 == 0:  # MUST BE MULTIPLE
                conts, _ = contours.sort_contours(row, method="left-to-right")
                magicSq_rows.append(conts)
                row = []

    #Storing Box Content into an Array
    boxContent = []
    for row in magicSq_rows:
        for i in row:
            mask = np.zeros(board.shape, dtype=np.uint8)
            cv2.drawContours(mask, [i], -1, (255, 255, 255), -1)
            result = cv2.bitwise_and(board, mask)
            result[mask == 0] = 255
            yippityyeppetyyep = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
            string = pytesseract.image_to_string(yippityyeppetyyep, config='--psm 6 --oem 1 -c tessedit_char_whitelist=0123456789')
            boxContent.append(string)
            cv2.waitKey(10)

    #Filtering the boxed array content into a readable array
    filteredArray = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    for i in range(len(boxContent)):
        filteredArray[i] = boxContent[i].replace('\n', '')

    if filteredArray.count(0) > 0:
        print("Illegal Magic Square")
        exit()

    return filteredArray



