import nltk
import os
import string
import math
import json
import warnings
import pandas as pd
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import logging 
 

#Global declarations
warnings.filterwarnings("ignore")
clear_command = "clear"
similarity_threshhold = 0.3
create_log_data = True
question_file = "largedataset.csv"
stopwords_file = "stopwords.txt"
log_file = "log.txt"
json_file = "output.json"
html_file = "/home/shriniwas/BE/BEProj/UI/driver.html"


logging.basicConfig( filename = log_file , format = "%(asctime)s %(message)s", filemode = "a") 
logger=logging.getLogger()   
logger.setLevel(logging.DEBUG)


class Questionclass:

	def __init__(self,question_id,title,question,link):
	
		self.question_id = question_id
		self.title = title
		self.question = question
		self.link = link
		self.similarity_score = 0
		self.vector = []
		
	def __lt__(self,question_obj):
	
		if(self.similarity_score < question_obj):	
			return True
			
		else:
			return False
		
	def __gt__(self,question_obj):
	
		if(self.similarity_score > question_obj):	
			return True
			
		else:
			return False


	def __eq__(self,question_obj):
	
		if(self.similarity_score == question_obj):	
			return True
			
		else:
			return False

	def __str__(self):
	
		return("\nQuestion id : {0}\nQuestion title : {1}\nQuestion : {2}\nSimilarity score : {3}\nVector : {4}\nLink : {5}".format(self.question_id,self.title,self.question,self.similarity_score,self.vector,self.link))



"""
input :
output :
functionality :
"""
def generate_stopwords_list(stopwords_file):

	if(create_log_data):
		logger.info("Starting generate_stopwords_list")

	stopwords_list = []

	try:
	
		fileobj = open(stopwords_file,"r")
	
	except:
	
		error_msg = "Error in openeing file " + stopwords_file
		
		if(create_log_data):
			logger.error(error_msg)
		
			
	list_of_lines = fileobj.readlines()
	stopwords_list = [x.split("\n")[0] for x in list_of_lines]
	
	if(create_log_data):
		logger.info("Completed generate_stopwords_list")
	
	return stopwords_list
	


"""
input :
output :
functionality :
"""
def caluculatesimilarity(vector_a,vector_b):

	if(create_log_data):
		logger.info("Starting caluculatesimilarity")

	set_of_words = set(vector_a)
	set_of_words = set_of_words | set(vector_b)
	
	binary_vec_a = []
	binary_vec_b = []
	
	for word in set_of_words:
	
		if(word in vector_a):
			binary_vec_a.append(1)
		else:
			binary_vec_a.append(0)


		if(word in vector_b):
			binary_vec_b.append(1)
		else:
			binary_vec_b.append(0)
	
	if(create_log_data):
		logger.info("Generated vectors")
	
	size_of_vector = len(binary_vec_a)
	
	similarity = sum([binary_vec_a[i] * binary_vec_b[i] for i in range(size_of_vector)])
	
	suma = 0
	sumb = 0
	
	for i in range(size_of_vector):
	 
		suma += (binary_vec_a[i]**2)
		sumb += (binary_vec_b[i]**2)	
	
	similarity /= math.sqrt(suma*sumb)
	
	if(create_log_data):
		logger.info("Completed caluculatesimilarity")
	
	return(similarity)


	
"""
input :
output :
functionality :
"""
def find_cosine_similarity(input_question_vector,list_of_questions):

	if(create_log_data):
		logger.info("Starting find_cosine_similarity")

	for question_object in list_of_questions:
	
		question_object.similarity_score = caluculatesimilarity(input_question_vector,question_object.vector)
				

	list_of_questions.sort(reverse = True)

	if(create_log_data):
		logger.info("Completed find_cosine_similarity")

	return list_of_questions



"""
input :
output :
functionality :
"""
def read_input():

	if(create_log_data):
		logger.info("Starting read_input")

	os.system(clear_command)
	print("\n\nEnter Question : \n\n\n")
	input_question = input()
	
	if(create_log_data):
		logger.info("Completed read_input")
	
	return input_question



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
def cleandata(input_question,list_of_question,stopwords_list):

	if(create_log_data):
		logger.info("Starting cleandata")

	ps = PorterStemmer()

	input_question = input_question.translate(str.maketrans('', '', string.punctuation)) 
	input_question_vector = word_tokenize(input_question)
	input_question_vector = [word.lower() for word in input_question_vector]
	input_question_vector = [ps.stem(word) for word in input_question_vector if not word in stopwords_list]
	
	for question_obj in list_of_question:
	
		clean_ques = question_obj.question.translate(str.maketrans('', '', string.punctuation))
		question_obj.vector = word_tokenize(clean_ques)
		question_obj.vector = [word.lower() for word in question_obj.vector]
		question_obj.vector = [ps.stem(word) for word in question_obj.vector if not word in stopwords_list]

	if(create_log_data):
		logger.info("Completed cleandata")

	return 	input_question_vector,list_of_questions
	


"""
input :
output :
functionality :
"""
def displayquestions(list_of_questions,input_question):

	os.system(clear_command)

	if(create_log_data):
		logger.info("Starting display questions")

	print("\nINPUT QUERY : " + input_question)

	print("\n\nRESULTS [SYNTACTIC]\n")
	print("===============================================================\n\n")
	print("SIMILARITY SCORE  :: QUESTION\n\n")
	
	for question in list_of_questions:
	
		#print("{0:.2f} :: ".format(question.similarity_score) + question.question + "\n")
		print(question)
	
	if(create_log_data):
		logger.info("Completed display questions")



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
			
			list_of_questions.append( Questionclass( int(dataframe.loc[i,"ID"]), dataframe.loc[i,"Title"], dataframe.loc[i,"Question"], dataframe.loc[i,"Link"]) )
		
	except:
		
		if(create_log_data):
			logger.info("Unable to open file : " + question_file)	


	if(create_log_data):
		logger.info("Completed readdatafromdb")

	return(list_of_questions)


"""
input :
output :
functionality :
"""
def createhtmlfile(list_of_questions,input_question,html_file,similarity_threshhold):

	try:
	
		fileobj = open(html_file,"w")
		
		fileobj.write("<html>\n\t<title> Question Links </title>\n<body>\n")
		fileobj.write("\nINPUT QUESTION : " + input_question + "\n\n<br><br><br>SUGGESTION QUESTIONS : <br><br>\n")
		
		for question in list_of_questions:
		
			if(question.similarity_score < similarity_threshhold):
			
				break
				
			fileobj.write("\n<a href = " + "\"" + question.link + "\">" + question.question + "</a>" + "<br>")
			
		fileobj.write("\n\n</body>\n</html>")
		fileobj.close()
		
	except:
		
		if(create_log_data):
			logger.info("Unable to open file : " + html_file)
	
	

###########################################################################################################	
"""
MAIN
"""
if (__name__ == "__main__"):		

	
	if(create_log_data):
		logger.info("=========================Starting MAIN===============================")

		
	list_of_questions = readdatafromdb(question_file) 	
	
	input_question = read_input()
	stopwords_list = generate_stopwords_list(stopwords_file)
	input_question_vector,list_of_questions = cleandata(input_question,list_of_questions,stopwords_list)
	list_of_questions = find_cosine_similarity(input_question_vector,list_of_questions)
	#displayquestions(list_of_questions,input_question)
	createhtmlfile(list_of_questions,input_question,html_file,similarity_threshhold)
	
	os.system("firefox " + html_file)
	
	if(create_log_data):
		logger.info("====================PROGRAM EXECUTION COMPLETED=====================")		
