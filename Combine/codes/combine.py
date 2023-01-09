"""
Author : Shriniwas Nayak

Date : 19th Feb 2020
"""


import logging
import os
import warnings
import pandas as pd
import copy

from combinequestionclass import Questionclass
from combinefileclass import FileClass
from combinelambdaclass import LambdaClass
from combinesyntactic import *
from combinesemantic import *
from combineutility import *


#Global declarations
warnings.filterwarnings("ignore")

# forward slash '/' for linux, backward slash '\' for windows, use '\\' (since \ is special character)
filenaming = "/"
clear_command = "clear"

create_log_data = True
create_json = True
create_graph = True

stopwords_file = "/home/shriniwas/BE/BEProj/Combine/input/stopwords.txt"
log_file = "/home/shriniwas/BE/BEProj/Combine/output/log.txt"
json_file = "/home/shriniwas/BE/BEProj/Combine/output/output.json"
graph_file = "/home/shriniwas/BE/BEProj/Combine/output/similarity_graph.png"
driver_filename = "/home/shriniwas/BE/BEProj/Combine/input/fileinfo.txt"

number_to_display = 5

#initalizing value of weight for syntactic
W = 0.5

logging.basicConfig( filename = log_file , format = "%(asctime)s %(message)s", filemode = "a") 
logger=logging.getLogger("MAIN MODULE")   
logger.setLevel(logging.DEBUG)


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
functionality :
"""
def displayquestions(list_of_questions,number_to_display):


	if(create_log_data):
		logger.info("Starting display questions")

	print("\n\nSIMILAR QUESTIONS \n")
	print("===============================================================\n\n")

	for i in range(min(len(list_of_questions),number_to_display)):
		
		print("{0:.2f} :: ".format(list_of_questions[i].similarity_score_combine) + list_of_questions[i].question+"\n" + "{0:.2f} Syntactic Score, {1:.2f} Semantic Score".format(list_of_questions[i].similarity_score_syn,list_of_questions[i].similarity_score_sem))
		print("\n\n")

			
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
			
			list_of_questions.append( Questionclass( int(dataframe.loc[i,"ID"]), dataframe.loc[i,"Title"], dataframe.loc[i,"Question"] ) )
		
	except:
		
		if(create_log_data):
			logger.info("Unable to open file : " + question_file)	


	if(create_log_data):
		logger.info("Completed readdatafromdb")

	return(list_of_questions)


###########################################################################################################	
"""
MAIN
"""
if (__name__ == "__main__"):		

	
	if(create_log_data):
		logger.info("=========================Starting MAIN===============================")

	w2v_model = KeyedVectors.load_word2vec_format(model_path, binary=True)

	while(True):

		if(create_log_data):
			logger.info("Inside Main Menu")
		
		os.system(clear_command)
		question_file = input("\n\nEnter file name or press 0 to exit : ")
		
		if(question_file == "0"):
			break

		while(True):

			os.system(clear_command)
			input_question = input("\n\nEnter question : ") 

			
			list_of_questions_syn = readdatafromdb(question_file)		
			list_of_questions_sem = copy.deepcopy(list_of_questions_syn)
				
			list_of_questions_syn = syntactic_similarity_operation(list_of_questions_syn,input_question,stopwords_file)
			list_of_questions_sem = semantic_similarity_operation(w2v_model,list_of_questions_sem,input_question,stopwords_file)
			
			combine_list_of_questions = [0 for iterator in range(len(list_of_questions_syn))]
		
			for question_obj in list_of_questions_syn:
			
				combine_list_of_questions[question_obj.question_id - 1] = LambdaClass(question_obj.question_id,question_obj.title,question_obj.question)
				combine_list_of_questions[question_obj.question_id - 1].similarity_score_syn = question_obj.similarity_score 
			
			for question_obj in list_of_questions_sem:
			
				combine_list_of_questions[question_obj.question_id -1].similarity_score_sem = float(question_obj.similarity_score)	
				combine_list_of_questions[question_obj.question_id -1].similarity_score_combine = (combine_list_of_questions[question_obj.question_id - 1].similarity_score_syn * W) + ((1-W)*combine_list_of_questions[question_obj.question_id - 1].similarity_score_sem) 
			
			combine_list_of_questions.sort(reverse = True)
					
			displayquestions(combine_list_of_questions,number_to_display)

			if(input("Press 1 for another question, any key to exit : ") != "1"):
				break


	if(create_json):
		createjason(input_question,combine_list_of_questions,json_file)
			
	if(create_graph):
		createGraph(combine_list_of_questions,graph_file)

	os.system(clear_command)

	
	if(create_log_data):
		logger.info("====================PROGRAM EXECUTION COMPLETED=====================")
	
