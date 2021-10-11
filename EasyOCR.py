import numpy as np
import pytesseract
import cv2
import os 
import sys
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
import functools
from googletrans import Translator

def main():
    translator = Translator(service_urls=['translate.googleapis.com'])
    nltk.download('punkt',quiet=True)
    nltk.download('wordnet',quiet = True)
    test_pic = Receipt('ahreceipt.jpg')
    
    #date functionality needs to be fixed
    # matches = re.findall(r'\d+[/.-]\d+[\.-]\d+',test_pic.text)
    # st = ' '
    # date = st.join(matches)
    sent_tokens = nltk.sent_tokenize(test_pic.text)
    sent_tokens = list(itertools.chain(*[new_item.split('\n') for new_item in sent_tokens]))
    #TODO:
    #Fix this hardcoded store-name thing
    #This is hardcoded FIX
    store_name = sent_tokens[0]
    price_str = [price for price in sent_tokens if ('totaal: ' or 'totaal' in price)]
    price = [total for total in price_str if ('totaal' in total)] #price_str[0][:-4] 
    bad_items = ['', ' ']
    date = 0
    filtered = [w for w in sent_tokens if w not in bad_items]


    #English to Dutch
    def quick_translate(word):
        return translator.translate(word, dest = 'nl').text


    potentials = ['entertainment','home','grocery']
    def syn_setmaker(synonym):
        syns = []
        
        for syn in wordnet.synsets(synonym):
            
            test1 = [quick_translate(word2) for word2 in [word1.name() for word1 in syn.lemmas()]]
            if test1 == [word1.name() for word1 in syn.lemmas()]:
                syns+=test1
            else:
                syns=[word1.name() for word1 in syn.lemmas()]+test1
           
            
            
        additional = []
        stores = []
        if synonym =='entertainment':
            additional = ['fun','restaurant','movie','cinema','park','hotel','room','meal','dinner']
            stores = ['Pathé', 'Best Western', 'IMAX', 'bar', 'pub' ]
        if synonym == "home":
            additional = ['internet','telephone','electricity','meter','wifi','consumer','reading','gas','water']

        if synonym == 'grocery':
            additional = ['milk','sugar','flour','soda','bread']
            stores = ['Albert Heijn','Albert', 'Heijn','Jumbo']
        
        #MUST BE EXPANDED LATER
        additional_nl = [quick_translate(word).lower() for word in additional]
        # print(syns + additional_nl + stores +additional)
        return [syn.lower() for syn in syns] + additional_nl + [store.lower() for store in stores] +[add.lower() for add in additional]
    
    def csv_maker(category,row):
        
        print(str(category) + ' category')
        filename = '{}.csv'.format(category)
        with open(filename, 'a+',newline='') as write_obj:
            csv_writer = csv.writer(write_obj)
            csv_writer.writerow(row)

    done = False
    # print(potentials)
    for w in potentials:
        total_set = syn_setmaker(w)
        for x in filtered:
            
            if x in total_set:
                print(x)
                done = True
                break
        if done ==True:
            receipt_type = w  
            csv_maker(receipt_type,[receipt_type,store_name,price])   
            break
    if done == False:
        receipt_type = 'other'
        csv_maker(receipt_type,[receipt_type,store_name,price])
    #Not sure if this will work, but if it does that'd be pretty cool
    # for y in potentials:

    #     exec("%s = %d" % (y, pd.read_csv(y+'.csv')))
    #     # y['Date']=pd.to_datetime(y.Date)
    #     y.head()

    # word_tokenized = word_tokenize(sent_tokens)
    







if __name__ == '__main__':
    main()