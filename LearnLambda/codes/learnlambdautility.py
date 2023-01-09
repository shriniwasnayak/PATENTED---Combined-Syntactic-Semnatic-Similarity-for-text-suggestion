"""
Author : Shriniwas Nayak

Date : 14th March 2020
"""



import logging
import os
import matplotlib.pyplot as plt
import json
from learnlambdaquestionclass import Questionclass


#Global declarations
log_file = "/home/shriniwas/BE/BEProj/LearnLambda/output/log.txt"
create_log_data = True


logging.basicConfig( filename = log_file , format = "%(asctime)s %(message)s", filemode = "a") 
logger=logging.getLogger("utility module")   
logger.setLevel(logging.DEBUG)



"""
input :
output :
functionality :
"""
def createGraph(Llist,srdslist,graph_file):

	if(create_log_data):
		logger.info("Starting createGraph")

	count_list = []

	plt.plot(Llist,srdslist)
	plt.xlabel("Value of Lambda")
	plt.ylabel("SRDS Value")
	plt.savefig(graph_file)
	plt.clf()	

	if(create_log_data):
		logger.info("Completed createGraph")


		
"""
input :
output :
functionality :
"""
def createjason(input_question,list_of_questions,json_file):

	if(create_log_data):
		logger.info("Starting create json")

	analysis_dictionary = {}
	analysis_dictionary["Input Question"] = input_question
	
	analysis_list_of_questions = []	 

			
	for i in range(len(list_of_questions)):
		
		temporary_dict = {"id" : list_of_questions[i].question_id, "title" : list_of_questions[i].title, "Question" : list_of_questions[i].question, "Combine Similarity score" : list_of_questions[i].similarity_score_combine, "Syntactic Similarity score" : list_of_questions[i].similarity_score_syn, "Semantic Similarity score" : list_of_questions[i].similarity_score_sem}

		analysis_list_of_questions.append(temporary_dict)
					
	
	analysis_dictionary["Suggested Questions"] = analysis_list_of_questions
		
	json_data = json.dumps(analysis_dictionary, indent = 4)		
	
	fileobj = None
	
	try:
	
		fileobj = open(json_file,"a")		
			
	except:
	
		if(create_log_data):
			logger.error("Unable to open file : " + json_file)		
	
		exit(1)
	
	fileobj.write(json_data)
		
	if(create_log_data):
		logger.info("Completed create json")	



"""
input :
output :
functionality :
"""
def generate_stopwords_list(stopwords_file):

	if(create_log_data):
		logger.info("Starting generate_stopwords_list")

	stopwords_list = []

	fileobj = None

	try:
	
		fileobj = open(stopwords_file,"r")
	
	except:
	
		error_msg = "Error in openeing file " + stopwords_file
		
		if(create_log_data):
			logger.error(error_msg)
			
		exit(1)
		
			
	list_of_lines = fileobj.readlines()
	stopwords_list = [x.split("\n")[0] for x in list_of_lines]
	
	if(create_log_data):
		logger.info("Completed generate_stopwords_list")
	
	return stopwords_list
