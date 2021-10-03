from math import *
import sqlite3


db = sqlite3.connect('User_DataBase.db')


def updateSqliteTable(receipt_items: list):

    try:
        
        cursor = db.cursor()
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS receipt_items
                        (item_name text PRIMARY KEY, amount real, price real)''')
        

        cursor.executemany('''INSERT OR IGNORE INTO receipt_items VALUES (?,?,?)''', receipt_items)



    except sqlite3.Error as error:
        print("Failed to update sqlite table", error)
    finally:
        if db:
            db.close()
            print("The sqlite connection is closed")

