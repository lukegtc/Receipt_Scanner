import pytesseract
import cv2
import os 
cwd = os.getcwd()


class Receipt:
    def __init__(self,image,folder:str = 'receipt_pics',lang:str = 'en'):
        self.path = cwd + '\\' +folder +'\\'+ image
        self.im_name = image
        self.image = cv2.imread(self.path)

    def processing(self):
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGRA2GRAY)
        #Sends gray image to gray file
        cv2.imwrite(cwd+'\\'+'gray'+'\\'+'gray'+self.im_name,self.gray)
        self.blur = cv2.GaussianBlur(self.gray,(7,7),0)
        cv2.imwrite(cwd+'\\'+'blur'+'\\'+'blur'+self.im_name,self.blur)

    def boxing(self):
        self.thresholded = cv2.threshold(self.blur,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
        cv2.imwrite(cwd+'\\'+'threshholded'+'\\'+'threshholded'+self.im_name,self.thresholded)

    def kernal(self):
        self.kernalled = cv2.getStructuringElement(cv2.MORPH_RECT,(3,13))
        cv2.imwrite(cwd+'\\'+'kernalled'+'\\'+'kernalled'+self.im_name,self.kernalled)
    

    def dilate(self,iterations=100):
        self.dilated = cv2.dilate(self.thresholded,self.kernalled,iterations)

        #Shrinking the gaps between the letters and numbers so that contouring will be easier
        self.closing = cv2.morphologyEx(self.dilated, cv2.MORPH_CLOSE, self.kernalled)
        cv2.imwrite(cwd+'\\'+'dilated'+'\\'+'dilated'+self.im_name,self.closing)        

    def contour(self,visualize = 0,min_h = 15, min_w = 1):
        self.contours = cv2.findContours(self.dilated,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.contours = self.contours[0] if len(self.contours) == 2 else self.contours[0]
        self.contours = sorted(self.contours, key=lambda x: cv2.boundingRect(x)[0])

        if visualize == 1:
            for contour in self.contours:
                x,y,w,h = cv2.boundingRect(contour)
                if h > min_h and w > min_w:
                    roi = self.image[y:y+h,x:x+h]
                    cv2.rectangle(self.image,(x,y), (x+w,y+h), (0,255,0),2)
        cv2.imwrite(cwd+'\\'+'contoured'+'\\'+'contoured'+self.im_name,self.image) 
#TODO: 
# Label the functions

if __name__ == '__main__':
    im1 = Receipt('ahreceipt2.jpg')
    # print(im1.txt_extract)
    im1.processing()
    im1.boxing()
    im1.kernal()
    im1.dilate()
    im1.contour(1)