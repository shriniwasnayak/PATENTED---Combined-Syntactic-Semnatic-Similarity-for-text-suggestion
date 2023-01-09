from flask import Flask, render_template,redirect,url_for,request
import nltk
import os
import string
import math
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from codes import product
from codes import productfileclass
from codes import productquestionclass
from codes import productsemantic
from codes import productsyntactic
from codes import productutility

#Global declarations
clear_command = "clear"
similarity_threshhold = 0.0
create_log_data = False
#question_file = "testinputdata.csv"
#stopwords_file = "stopwords.txt"
inputques=''
s1,s2,s3=0,0,0
q1,q2,q3='','',''
i=1


app = Flask(__name__)
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/',methods=['POST'])
def getdata():
    inputques=request.form['name']
    #print('*************************************',question)

    #list_of_questions=product.readdatafromdb(question_file)
    input_question = inputques
    q1,s1,q2,s2,q3,s3=product.maincode(input_question)
    #return render_template('answer.html')        
    #************************************************
    return render_template('answer.html',ques=input_question,q11=q1,s11=s1,q22=q2,s22=s2,q33=q3,s33=s3)

@app.route('/answer')
def answer(question):
    #return render_template(question)
    return render_template('answer.html')
#*************************************************************************
#**************************************************************************

if __name__ == '__main__':
    app.run(debug=True)
    
    