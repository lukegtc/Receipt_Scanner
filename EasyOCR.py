import numpy as np
import pytesseract
import cv2
import os 
from PIL import Image
import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import csv
import nltk
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import wordnet
from OCR_Processing import Receipt
import itertools
from googletrans import Translator
def main():
    translator = Translator()
    nltk.download('punkt',quiet=True)
    nltk.download('wordnet',quiet = True)
    test_pic = Receipt('irl_pic.jpg')
    
    #date functionality needs to be fixed
    # matches = re.findall(r'\d+[/.-]\d+[\.-]\d+',test_pic.text)
    # st = ' '
    # date = st.join(matches)
    sent_tokens = nltk.sent_tokenize(test_pic.text)
    sent_tokens = list(itertools.chain(*[new_item.split('\n') for new_item in sent_tokens]))
    # print(sent_tokens)
    store_name = sent_tokens[0][0]
    price_str = [price[8:] for price in sent_tokens if ('totaal: ' in price)]
    price = price_str[0][:-4] 
    bad_items = ['', ' ']
    date = 0
    filtered = [w for w in sent_tokens if w not in bad_items]


    potentials = ['entertainment','home','grocery']
    def syn_setmaker(synonym):
        syns = []
        for syn in wordnet.synsets(synonym):
            for lem in syn.lemmas():
                print(lem.name())
#-----------------#IT'S BROKEN HERE------------------------------
                syns.append(translator.translate(lem.name()))#, src = 'nl')) IT'S BROKEN HERE
        additional = []
        stores = []
        if synonym =='entertainment':
            additional = ['fun','restaurant','movie','cinema','park','hotel','room','meal','dinner']
            stores = ['Pathé', 'Best Western', 'IMAX', 'bar', 'pub' ]
        if synonym == "home":
            additional = ['intnernet','telephone','electricity','meter','wifi','consumer','reading','gas','water']

        if synonym == 'grocery':
            additional = ['milk','sugar','flour','soda','bread']
            stores = ['Albert Heijn','Albert', 'Heijn','Jumbo']
        
        #MUST BE EXPANDED LATER
        additional_nl = [translator.translate(word) for word in additional]
        return syns + additional_nl + stores
    
    def csv_maker(category,row):
        
        print(str(category) + 'category')
        filename = '{}.csv'.format(category)
        with open(filename, 'a+',newline='') as write_obj:
            csv_writer = csv.writer(write_obj)
            csv_writer.writerow(row)






    done = False
    for w in potentials:
        for x in filtered:
            if x in syn_setmaker(w):
                done = True
                break
        if done ==True:
            receipt_type = w     
            break
    if done == False:
        receipt_type = 'other'

    csv_maker(receipt_type,[receipt_type,store_name,price])
    #Not sure if this will work, but if it does that'd be pretty cool
    for y in potentials:
        exec("%s = %d" % (y, pd.read_csv(y+'.csv')))
        y['Date']=pd.to_datetime(y.Date)
        y.head()

    # word_tokenized = word_tokenize(sent_tokens)








if __name__ == '__main__':
    main()