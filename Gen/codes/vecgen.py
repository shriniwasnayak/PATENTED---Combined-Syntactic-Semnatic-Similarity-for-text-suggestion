import nltk
import os
import string
import math
import warnings
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import logging 
import random 

#Global declarations
warnings.filterwarnings("ignore")
clear_command = "clear"
create_log_data = True
question_file = "/home/shriniwas/BE/BEProj/Gen/input/largeinputdata.csv"
log_file = "/home/shriniwas/BE/BEProj/Gen/output/log.txt"

number_of_questions = 20

logging.basicConfig( filename = log_file , format = "%(asctime)s %(message)s", filemode = "a") 
logger=logging.getLogger()   
logger.setLevel(logging.DEBUG)


class Questionclass:

	def __init__(self,question_id,title,question):
	
		self.question_id = question_id
		self.title = title
		self.question = question
		self.clean_question = ""	
		self.vector = []
		
	
	def __str__(self):
	
		return("\nQuestion id : {0}\nQuestion title : {1}\nQuestion : {2}\nClean Question : {3}\nVector : {4}".format(self.question_id,self.title,self.question,self.clean_question,self.vector))



"""
input :
output :
functionality :
"""
def readdatafromdb(question_file):

	list_of_questions = []

	if(create_log_data):
		logger.info("Starting readdatafromdb")

	try:
	
		dataframe = pd.read_csv(question_file)
		
		for i in range(len(dataframe)):
			
			list_of_questions.append( Questionclass( int(dataframe.loc[i,"ID"]), dataframe.loc[i,"Title"], dataframe.loc[i,"Question"] ) )
		
	except:
		
		if(create_log_data):
			logger.info("Unable to open file : " + question_file)
			
		exit(1)	


	if(create_log_data):
		logger.info("Completed readdatafromdb")

	return(list_of_questions)




"""
input :

output :

functionality : Performs following for input and database questions -
1) Removes Punctuation marks
2) converts data in lower case
3) Creates Tokens
4) Removes stop words
5) Performs Stemming 
6) Creates vector of words
"""
def cleandata(list_of_questions):

	if(create_log_data):
		logger.info("Starting cleandata")

	ps = PorterStemmer()
	
	for question_obj in list_of_questions:
	
		clean_ques = question_obj.question.translate(str.maketrans('', '', string.punctuation))
		question_obj.vector = word_tokenize(clean_ques)
		question_obj.vector = [word.lower() for word in question_obj.vector]
		question_obj.clean_question = " ".join(question_obj.vector)
		
	if(create_log_data):
		logger.info("Completed cleandata")

	return 	list_of_questions



"""
input :
output :
functionality :
"""
def create_questions(list_of_questions,start_cluster,number_of_questions):

	start_list = []
	body_list = []
	
	for question in list_of_questions:
	
		sentence = question.clean_question
		
		temp_str = ""
		
		size = len(sentence)
		
		for index in range(0,size):
		
			temp_str += sentence[index]
			
			if(temp_str in start_cluster):

				start_list.append(temp_str)
				body_list.append(sentence[min(index+1,size-1):])
	
	generated_questions_list = []
	
	for iteration in range(number_of_questions):
	
		 generated_questions_list.append(random.choice(start_cluster) + random.choice(body_list))
	
	return generated_questions_list
				
				

###########################################################################################################	
"""
MAIN
"""
if (__name__ == "__main__"):		

	
	if(create_log_data):
		logger.info("=========================Starting MAIN===============================")

	
	start_cluster = ["what is","how is","where is","when is","who is","why is","what to","how to","where to","when to","who to","why to","how can","unable to","who can","how do","what do","where do"]
		
	list_of_questions = readdatafromdb(question_file) 	
	list_of_questions = cleandata(list_of_questions)
	
	generated_questions_list = create_questions(list_of_questions,start_cluster,number_of_questions)
	
	print("\n\nGenerated questions are : \n\n\n")
	
	for question in generated_questions_list:
	
		print(question,end="")
	
		for obj in list_of_questions:
		
			if (question == obj.clean_question):
				
				print(" :: Already in DB",end="")
				
		print("\n\n",end="")
		

	print("\n\n")

	if(create_log_data):
		logger.info("====================PROGRAM EXECUTION COMPLETED=====================")
		
