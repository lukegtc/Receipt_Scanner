from math import *
import numpy as np
import easyocr
import cv2
import os
import matplotlib.pyplot as plt
im_set = 0
cwd = os.getcwd()
class Image:
    def __init__(self,image,folder:str = 'receipt_pics',lang:str = 'en'):
        self.path = cwd + '\\' +folder +'\\'+ image
        #image to ocr text locations and text
        self.txt_extract = easyocr.Reader([lang],gpu=False).readtext(self.path)

    def visualize(self):
        img = cv2.imread(self.path)
        for item in self.txt_extract:
            top_left = tuple([int(val) for val in item[0][0]])
            bottom_right = tuple([int(val) for val in item[0][2]])
            text = item[1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            img = cv2.rectangle(img, top_left,bottom_right,(0,255,0),5)
            img = cv2.putText(img,text, top_left,font, 0.45, (0,0,255), 1, cv2.LINE_AA)
        plt.figure(figsize=(10,10))
        plt.imshow(img)
        plt.show()
if __name__ == '__main__':
    im1 = Image('ahreceipt2.jpg')
    # print(im1.txt_extract)
    im1.visualize()