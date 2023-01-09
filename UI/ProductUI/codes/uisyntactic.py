"""
Author : Shriniwas Nayak

Date : 18th Feb 2020
"""

import logging
import nltk
import os
import string
import math
import pandas as pd
import warnings

from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

from uiquestionclass import Questionclass
from uiutility import *


#Global declarations
log_file = "/home/shriniwas/BE/BEProj/UI/ProductUI/output/log.txt"
stopwords_file = "/home/shriniwas/BE/BEProj/UI/ProductUI/input/stopwords.txt"

create_log_data = True


logging.basicConfig( filename = log_file , format = "%(asctime)s %(message)s", filemode = "a") 
logger=logging.getLogger("SYNTACTIC MODULE")   
logger.setLevel(logging.DEBUG)
	

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
def cleandata(list_of_questions,stopwords_list):

	if(create_log_data):
		logger.info("Starting cleandata")

	ps = PorterStemmer()
	
	for question_obj in list_of_questions:
	
		clean_ques = question_obj.question.translate(str.maketrans('', '', string.punctuation))
		question_obj.vector = word_tokenize(clean_ques)
		question_obj.vector = [word.lower() for word in question_obj.vector]
		question_obj.vector = [ps.stem(word) for word in question_obj.vector if not word in stopwords_list]

	if(create_log_data):
		logger.info("Completed cleandata")

	return 	list_of_questions



"""
input :
output :
functionality :
"""
def cleaninputquestion(input_question,stopwords_list):

	if(create_log_data):
		logger.info("Starting cleaninputquestion")

	ps = PorterStemmer()

	input_question = input_question.translate(str.maketrans('', '', string.punctuation)) 
	input_question_vector = word_tokenize(input_question)
	input_question_vector = [word.lower() for word in input_question_vector]
	input_question_vector = [ps.stem(word) for word in input_question_vector if not word in stopwords_list]


	if(create_log_data):
		logger.info("Completed cleaninputquestion")
			
	return 	input_question_vector


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
def syntactic_similarity_operation(list_of_questions,input_question,stopwords_file):

	if(create_log_data):
		logger.info("Starting syntactic_similarity_operation")

	type_of_operation = "(SYNTACTIC)"

	stopwords_list = generate_stopwords_list(stopwords_file)
	list_of_questions = cleandata(list_of_questions,stopwords_list)
	
	input_question_vector = cleaninputquestion(input_question,stopwords_list)
	list_of_questions = find_cosine_similarity(input_question_vector,list_of_questions)
	
	
	if(create_log_data):
		logger.info("Completed syntactic_similarity_operation")
		
	return list_of_questions
	
