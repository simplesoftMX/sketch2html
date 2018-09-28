from PIL import Image
import re
import cv2
import random
import numpy as np
import pytesseract

width = 800
height = 600

def mser(roi_img):
    ## Read image and change the color space
    img = roi_img
    #vis = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, viss = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    #cv2.imwrite("html/" + 'view0.jpg', viss)
    e = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 1))
    viss = cv2.dilate(viss, e, iterations=1)
    #cv2.imwrite("html/" + 'view1.jpg', viss)
    e = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 5))
    viss = cv2.erode(viss, e, iterations=1)
    #cv2.imwrite("html/" + 'view2.jpg', viss)
    e = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 1))
    viss = cv2.dilate(viss, e, iterations=3)
    #cv2.imwrite("html/" + 'view3.jpg', viss)

    viss, contours, hierarchy = cv2.findContours(viss, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    viss = cv2.drawContours(viss, contours, -1, (255, 255, 255), 2)
    #print (contours)
    areaSize=[]
    for contour in contours:
        currentArea = cv2.contourArea(contour)
        areaSize.append(currentArea)
        #print(currentArea)

    avg=sum(areaSize)/len(areaSize)
    objectCountor=0
    for item in areaSize:
        if item>(avg/2):
            objectCountor+=1
    return objectCountor

def cleanText(origin_text):
    text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', origin_text)
    return text

def textMser(img, mode = "findpos", offset = 10):
    # img = cv2.imread(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #Converting to GrayScale
    text = cleanText(pytesseract.image_to_boxes(gray, config="--psm 11 --oem 1"))
    text = text.split("\n")
    array = []
    for m in text:
        info = m.split(" ")
        x1, y1, x2, y2 = int(info[1]) - offset, int(height - int(info[4])) - offset, int(info[3]) + offset, int(height - int(info[2])) + offset
        info = [info[0], [x1, y1, x2, y2]]
        array.append(info)
    index = 0
    if mode.lower() == "findword":
        while index < len(array) - 1:
            if abs(array[index][1][1] - array[index + 1][1][1]) <= offset and abs(array[index][1][2] - array[index + 1][1][0]) <= 2 * offset:
                str = array[index][0] + array[index + 1][0]
                temp = [str, [int(array[index][1][0]), int(array[index][1][1]), int(array[index + 1][1][2]), int(array[index + 1][1][3])]]
                array[index] = temp
                array.pop(index + 1)
                index -= 1
            index += 1
    elif mode.lower() == "findpos":
        while index < len(array) - 1:
            if abs(array[index][1][1] - array[index + 1][1][1]) <= offset and abs(array[index][1][2] - array[index + 1][1][0]) <= 2 * offset:
                str = "ocrtext"
                temp = [str, [int(array[index][1][0]), int(array[index][1][1]), int(array[index + 1][1][2]), int(array[index + 1][1][3])]]
                array[index] = temp
                array.pop(index + 1)
                index -= 1
            index += 1
    # print(array)
    return array

if __name__=='__main__':
    # origin = cv2.imread("./html/radioButtonV.jpg")
    # returning = mser(origin)
    # print("검출 : ", returning)
    textMser('onlyTextimg.jpg', "findword")
