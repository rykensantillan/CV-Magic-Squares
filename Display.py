"""
Made by: Ryken Santillan
Version Started: 2022-12-30
Version Finished: 2022-12-31
Class: Display
Description:
      - This class produces an image result of the solved magic square
      - Included is: font optimization, text centering
"""

import cv2
import numpy as np

#Creates blank
def create(width, height, rgb_color=(0, 0, 0)):
    image = np.zeros((height, width, 3), np.uint8)
    color = tuple(reversed(rgb_color))
    image[:] = color
    return image

#gets best possible font considering array of numbers
def get_font(array, width):
    arrMax = 0
    #Find max number in list
    for i in range(len(array)):
        if int(array[i]) > arrMax:
            arrMax = int(array[i])

    for scale in reversed(range(60)):
        textSize = cv2.getTextSize(str(arrMax), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=scale/10, thickness=1)
        new_width = textSize[0][0]
        if new_width <= width:
            return scale/10
    return 1

#gets centred coordinates in each box of 200 x 200 depending on text size
def get_centred_coordinates(text, scale):
    textSize, _ = cv2.getTextSize(text, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=scale, thickness=1)
    width, height = textSize
    idealWidth = int((200 - width)/2)
    idealHeight = int(((200 - height)/2) + height)

    return idealWidth, idealHeight

# four parameters are to specify each row...
def produceText(arr, arrInd, size, image):
    j = 0
    if (arrInd[1] > 3): k = 200
    else: k = 0
    if (arrInd[1] > 6): l = 200
    else: l = 0

    #Loop to place text on image
    for i in range(arrInd[0], arrInd[1], arrInd[2]):
        coords = get_centred_coordinates(f'{arr[i]}', size)
        cv2.putText(image, f'{arr[i]}', (coords[0]+(j*200),coords[1]+(k) + (l)), cv2.FONT_HERSHEY_SIMPLEX, size, (36,255,12), 2)
        j+=1

# image is produced and stays until closed via 'q'
def produceImg(arr):
    # Create 600 x 600 white image
    image = create(600, 600, rgb_color=(255,255,255))

    # Creating Rectangles that will define our magic squares board
    for i in range(0, 600, 200):
        row1 = cv2.rectangle(image, (0 + i, 0), (200 + i, 200), (0, 0, 0), 1)
        row2 = cv2.rectangle(image, (0 + i, 200), (200 + i, 400), (0, 0, 0), 1)
        row3 = cv2.rectangle(image, (0 + i, 400), (200 + i, 600), (0, 0, 0), 1)

    size = get_font(arr, 100)
    produceText(arr, [0,3,1], size, image)
    produceText(arr, [3,6,1], size, image)
    produceText(arr, [6,9,1], size, image)
    cv2.imshow('Solved Result', image)

    cv2.waitKey(0)
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()