from math import *
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import pandas as pd
import requests
key = '2068120405:AAGkFNOajfhBe45wq7rgrWrnU4UQe7aAHJM'
method = "getupdates"
file_path = ""

cwd = os.getcwd()
dir = "telegram_pics"
response = requests.get(f"https://api.telegram.org/bot{key}/{method}")

file_id = response.json()['result'][2]['message']['photo'][0]['file_id']
file_data = requests.get(f"https://api.telegram.org/bot{key}/getFile?file_id={file_id}")
print(file_data.json())
file = file_data.json()['result']['file_path']
file_download = requests.get(f"https://api.telegram.org/file/bot{key}/{file}")


