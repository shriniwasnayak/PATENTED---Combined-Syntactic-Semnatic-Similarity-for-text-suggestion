from flask import Flask, render_template,redirect,url_for,request
import nltk
import os
import string
import math
import pandas as pd
from gensim.models.keyedvectors import KeyedVectors
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from codes import combine
from codes import load
from codes import combinefileclass
from codes import combinequestionclass
from codes import combinesemantic
from codes import combinesyntactic
from codes import combinelambdaclass
from codes import combineutility

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
model_path = '/home/shriniwas/BE/BEProj/UI/Flask/input/GoogleNews-vectors-negative300.bin'
#w2v_model = KeyedVectors.load_word2vec_format(model_path, binary=True)
inputfile=""

#=========================
app = Flask(__name__)
app.config['DEBUG'] = True

class DataStore():
    w2v_model = None

data = DataStore()

@app.route('/cq',methods=['POST'])
def cq():
    inputfile=request.form['questfile']
    return render_template('home.html',inputfile=inputfile)

@app.route('/')
def home1():
    return render_template('home.html',inputfile=inputfile)

@app.route('/home',methods=['POST'])
def home():
    inputfile=request.form['questfile']
    #inputfile=$value
    return render_template('home.html',inputfile=inputfile)

@app.route('/select')
def select():
    #w2v_model = request.args.get('w2v_model', None)
    return render_template('fileselection.html')

@app.route('/fileselect',methods=['POST'])
def fileselect():
    #w2v_model = request.args.get('w2v_model', None)
    return render_template('fileselection.html')

@app.route('/loading')
def loading():
    w2v_model=load.main()
    data.w2v_model=w2v_model
    #return redirect(url_for('select'),w2v_model=w2v_model)
    return render_template('fileselection.html')

@app.route('/',methods=['POST'])
def getdata():
    inputques=request.form['name']
    inputfile=request.form['questfile']
    #inputfile = request.args.get('inputfile', None)
    #print('*************************************',question)
    #w2v_model = request.args.get('w2v_model')
    #list_of_questions=combine.readdatafromdb(question_file)
    input_question = inputques
    #q1,s1,q2,s2,q3,s3=combine.maincode(input_question)
    q1,s1,l1,q2,s2,l2,q3,s3,l3=combine.maincode(input_question,inputfile,data.w2v_model)
    #return render_template('answer.html')        
    #************************************************
    return render_template('answer.html',ques=input_question,q11=q1,s11=s1,l11=l1,q22=q2,s22=s2,l22=l2,q33=q3,s33=s3,l33=l3,inputfile=inputfile)

@app.route('/answer')
def answer(question):
    #return render_template(question)
    return render_template('answer.html')
#*************************************************************************
#**************************************************************************

if __name__ == '__main__':
    app.run(debug=True)    
    
