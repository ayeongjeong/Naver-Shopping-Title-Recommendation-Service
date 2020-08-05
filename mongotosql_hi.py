import pandas as pd
import numpy as np
from pymongo import MongoClient

client = MongoClient('mongodb://192.168.0.154:27017/')  # mongo 연결
mydb = client.mydb

model_info = mydb.modelingdb.find() # get Collection with find()

import sqlite3

with sqlite3.connect('db.sqlite3') as con:
    cur = con.cursor()
    category = str()
    product = str()
    title = str()
    rank = str()
    for info in model_info :
        category = info['category']
        product = info['product']
        title = info['title']
        rank = info['rank']
        cur.execute('INSERT INTO modeling (category, product, title, rank) VALUES (?,?,?,?)', (category, product, title, rank))
    con.commit()