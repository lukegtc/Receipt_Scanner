from OCR_Processing import Receipt
import os 
cwd = os.getcwd()


filename = Receipt('ahreceipt.jpg')

with open(filename, 'rb') as f:
    print(f)