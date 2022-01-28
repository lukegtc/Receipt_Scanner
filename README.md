# Receipt_Scanner
A script that processes images to return the text on them, mainly receipts. Script then uses Telegram to receive images to process, then place into a spreadsheet.
The OCR_Processing.py file takes images and uses several image processing techniques while allocating these processed images to specific folders. Once processed the isolated characters are analyzed by a
character recognition neural network. The EasyOCR.py file does everythig the OCR_Processing.py file does, but condensed, as a built-in image processing function was used. 
