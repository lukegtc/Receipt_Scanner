from math import *
import sqlite3
import numpy as np
import pandas as pd

db = sqlite3.connect('books.db')

cur=  db.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS books(id integer PRIMARY KEY,
                title text NOT NULL,
                author text NOT NULL,
                price real);''')


cur.execute('''INSERT INTO books(id, title, author, price)
                VALUES('1','Untold Stories','Alan Bennett', '17.49')''')


book_list = [('2','Potato Joe', 'Bob Songs', '23.99'),
            ('3','Potato Joe 2 Spud Boogaloo', 'Bob Songs', '49.99')]

cur.executemany('''INSERT INTO books(id, title, author, price)
                VALUES(?,?,?,?) ''', book_list)

cur.execute('SELECT * FROM books')
print(cur.fetchall())

db.commit()
db.close()