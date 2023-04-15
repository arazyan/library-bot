import pandas as pd 
from flask import Flask 
from os import getcwd 
from database import * 
app = Flask(__name__) 
#connection = connection from database.py 
 
 
@app.route("/download/<book_id>", methods = ['GET']) 
def create_csv(book_id): 
    path = getcwd() 
    file_ = path +'/borrows.csv' 
    df = pd.read_sql(f"select * from Borrows where book_id = {book_id}", connection) 
    df.drop('user_id', axis = 1, inplace = True) 
    df.to_csv(file_, index = False, sep = ';') 
    return book_id 
app.run("0.0.0.0", port=8080)