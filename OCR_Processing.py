import numpy as np
import pytesseract
import cv2
import os 
cwd = os.getcwd()


class Receipt:
    """ path: current working directory + the associated folder and the (adjusted image)
        im_name: name of image
        image: Actual image"""
    def __init__(self,image,folder:str = 'receipt_pics',lang:str = 'en'):
        self.path = cwd + '\\' +folder +'\\'+ image
        self.im_name = image
        self.image = cv2.imread(self.path)
    
    '''clears all files in dir list (the junk files).'''
    def wipe(self,directories:list = ['gray','blur','thresholded','dilated','ROI_files','contoured']):
        for directory in directories:
            try:
                cwd1 = cwd + '\\'+directory
                
                for file in os.listdir(directory):
                    os.remove(cwd1 + '\\'+file)
            except PermissionError:
                print(str(cwd1 + '\\'+file),'not deleted') #May remove this print statement later
                continue


    """Sends image through a gray filter and a Gaussian blur filter. saves each into its respective file"""
    def processing(self):
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGRA2GRAY)
        cv2.imwrite(cwd+'\\'+'gray'+'\\'+'gray'+self.im_name,self.gray)

        self.blur = cv2.GaussianBlur(self.gray,(7,7),0)
        cv2.imwrite(cwd+'\\'+'blur'+'\\'+'blur'+self.im_name,self.blur)

    '''Assigns pixel black or white depending on which side of the threshold its on. Helps remove noise.'''
    def threshold(self):
        self.thresholded = cv2.threshold(self.blur,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
        cv2.imwrite(cwd+'\\'+'threshholded'+'\\'+'threshholded'+self.im_name,self.thresholded)

    '''Creates and sizes kernal'''
    def kernal(self):
        self.kernal = cv2.getStructuringElement(cv2.MORPH_RECT,(3,13))
    
    '''size of foreground objects increases, closes gaps in text'''
    def dilate(self,iterations=100):
        self.dilated = cv2.dilate(self.thresholded,self.kernal,iterations)

        #Shrinking the gaps between the letters and numbers so that contouring will be easier
        self.closing = cv2.morphologyEx(self.dilated, cv2.MORPH_CLOSE, self.kernal)
        cv2.imwrite(cwd+'\\'+'dilated'+'\\'+'dilated'+self.im_name,self.closing)        

    '''Finds contours and saves them to the contour file'''
    def contour(self,visualize = 0,min_h = 20, min_w = 5 ):
        self.contours = cv2.findContours(self.dilated,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.contours = self.contours[0] if len(self.contours) == 2 else self.contours[0]
        self.contours = sorted(self.contours, key=lambda x: cv2.boundingRect(x)[0])

        
        i = 0
        if not os.path.isdir(cwd+'\\'+'ROI_files'+'\\' + self.im_name): 
            os.mkdir(cwd+'\\'+'ROI_files'+'\\' + self.im_name)
        rois = []
        for contour in self.contours:
            x,y,w,h = cv2.boundingRect(contour)

            #Filters boxes

            if h > min_h and w > min_w:
                roi = self.image[y:y+h,x:x+h]
                rois.append(roi)
                if visualize == 1:
                    cv2.rectangle(self.image,(x,y), (x+w,y+h), (0,255,0),2)
                # cv2.imwrite(cwd+'\\'+'ROI_files'+'\\' + str(self.im_name)[:-4]+'\\'+'roi' + str(i) +self.im_name ,roi)
                i +=1
        self.rois = rois
        cv2.imwrite(cwd+'\\'+'contoured'+'\\'+'contoured'+self.im_name,self.image) 


    def im2str(self):
        for item in self.rois:
            ocr = pytesseract.image_to_string(item)
            ocr = ocr.split('\n')
            for val in ocr:
                val = val.strip()
                print(val)

#TODO: 
# Label the functions
# Streamline the file management
#


if __name__ == '__main__':
    im1 = Receipt('receipt.jpg')
    # print(im1.txt_extract)
    im1.wipe()
    im1.processing()
    im1.threshold()
    im1.kernal()
    im1.dilate()
    im1.contour()
    im1.im2str()