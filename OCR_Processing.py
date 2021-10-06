import numpy as np
import pytesseract
import cv2
import os 
cwd = os.getcwd()


class Receipt:
    """ path: current working directory + the associated folder and the (adjusted image)
        im_name: name of image
        image: Actual image"""
    def __init__(self,image,folder:str = 'receipt_pics'):
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
        self.thresholded = cv2.threshold(self.blur,100,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
        cv2.imwrite(cwd+'\\'+'thresholded'+'\\'+'thresholded'+self.im_name,self.thresholded)

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
    def contour(self,visualize = 0,min_h = 20, min_w = 5, max_h = 100):
        self.contours = cv2.findContours(self.dilated,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.contours = self.contours[0] #if len(self.contours) == 2 else self.contours[0]
        self.contours = sorted(self.contours, key=lambda x: cv2.boundingRect(x)[0])
    
        #This is gonna need to be optimized 
        def contour_combine():
            contour_set = self.contours
            cg_set = []
            new_contours = []
            for item in contour_set:
                x,y,w,h = cv2.boundingRect(item)
                cg_set.append((x+w/2,y+h/2,w,h))#,item)
            #Go through contour_set
            #Find closest characters in +- x direction
            
            while cg_set != []:
                margin = 1. 
                closest = []
                key_cg = cg_set[0]
                closest.append([[key_cg[0]-key_cg[2]/2,key_cg[1]+key_cg[3]/2]])
                for cg in cg_set[1:]:
                    
                    if key_cg[1]-key_cg[3]/2*margin<=cg[1]<=key_cg[1]+key_cg[3]/2*margin:
                        closest.append([[cg[0]-cg[2]/2,cg[1]-cg[3]/2]])
                        closest.append([[cg[0]+cg[2]/2,cg[1]+cg[3]/2]])
                        cg_set.remove(cg)
                cg_set.remove(key_cg)
              
                
                if len(closest) >=2:
                    new_box = cv2.boundingRect(np.array(closest,np.float32))
                    new_contours.append(new_box)
            return new_contours
        # Implement this code below but w contours that have cgs close to each other and to the right or left of each other
    
        # contours = np.vstack(contours)
        # print(self.contours)
        '''combining bounding boxes'''
        # a and b are boxes
        def union(a,b):
            x = min(a[0], b[0])
            y = min(a[1], b[1])
            w = max(a[0]+a[2], b[0]+b[2]) - x
            h = max(a[1]+a[3], b[1]+b[3]) - y
            return (x, y, w, h)

        def intersection(a,b):
            x = max(a[0], b[0])
            y = max(a[1], b[1])
            w = min(a[0]+a[2], b[0]+b[2]) - x
            h = min(a[1]+a[3], b[1]+b[3]) - y
            if w<0 or h<0: return () # or (0,0,0,0) ?
            return (x, y, w, h)
        
        # Uses the above functions to comine the nearest contours

        i = 0
        if not os.path.isdir(cwd+'\\'+'ROI_files'+'\\' + self.im_name): 
            os.mkdir(cwd+'\\'+'ROI_files'+'\\' + self.im_name)
        rois = []
        new_conts = contour_combine()
        for contour in new_conts:#self.contours:
            
            x,y,w,h = contour #cv2.boundingRect(contour)

            #Filters boxes
            margin_pixels = 0
            if True == True:#h > min_h and w > min_w:
                roi = self.image[y-margin_pixels:y+h+margin_pixels,x-margin_pixels:x+w+margin_pixels]
                rois.append(roi)
                if visualize == 1:
                    cv2.rectangle(self.image,(x,y), (x+w,y+h), (0,255,0),2)
                    # cv2.drawContours(self.image,[hull],0,(0,255,0),2)
                cv2.imwrite(cwd+'\\'+'ROI_files'+'\\' + str(self.im_name)+'\\'+'roi' + str(i) +self.im_name ,roi)
                i +=1
        self.rois = rois
        cv2.imwrite(cwd+'\\'+'contoured'+'\\'+'contoured'+self.im_name,self.image) 


    def im2str(self):
        ocr_out = []
        for item in self.rois:
            
            #Black Box that I need to learn more about
            #Will make my own AI for this in the near future

            
            ocr = pytesseract.image_to_string(item)
            
            ocr = ocr.split('\n')
            print(ocr)
            for val in ocr:
                if val!='\x0c' and val!=' ' and val!='':
                    ocr_out.append(val)
            
                # val = val.strip().replace("\n","")
                # val = val.split(" ")[0]
                # if val!= '\x0c' and len(val) > 0:
                #     ocr_out.append(val)
            
        print(ocr_out)   

#TODO: 
# Label the functions (kinda done)
# Streamline the file management
#Learn about the Black Box


if __name__ == '__main__':
    im1 = Receipt('irl_pic.jpg')
    # print(im1.txt_extract)
    im1.wipe()
    im1.processing()
    im1.threshold()
    im1.kernal()
    im1.dilate()
    im1.contour(1)
    # print(im1.contour().contour_combine()) #insert a 1 for a visualization in contoured folder
    im1.im2str()