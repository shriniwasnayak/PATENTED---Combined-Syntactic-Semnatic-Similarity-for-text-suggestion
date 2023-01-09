"""
Author : Shriniwas Nayak

Date : 18th Feb 2020
"""



import logging
import os
import matplotlib.pyplot as plt
import json
import string
import numpy
from uiquestionclass import Questionclass


#Global declarations
log_file = "/home/shriniwas/BE/BEProj/UI/ProductUI/output/log.txt"
create_log_data = True


logging.basicConfig( filename = log_file , format = "%(asctime)s %(message)s", filemode = "a") 
logger=logging.getLogger("utility module")   
logger.setLevel(logging.DEBUG)



"""
input :
output :
functionality :
"""
def createGraph(list_of_questions,graph_file):

	if(create_log_data):
		logger.info("Starting createGraph")

	count_list = []

	for question_object in list_of_questions:
	
		count_list.append(100*question_object.similarity_score)

	plt.hist(count_list,facecolor = "red")
	plt.xlabel("Similarity Percentage")
	plt.ylabel("Frequency")
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
		
		temporary_dict = {"id" : list_of_questions[i].question_id, "title" : list_of_questions[i].title, "Question" : list_of_questions[i].question, "Similarity score" : list_of_questions[i].similarity_score, "Vector" : list_of_questions[i].vector}

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
	
"""
input :
output :
functionality :
"""
def createhtmlfile(list_of_questions,input_question,html_file,number_to_display):

	try:
	
		fileobj = open(html_file,"w")
		
		fileobj.write("<html>\n\t<title> Question Links </title>\n<body>\n")
		fileobj.write("\nINPUT QUESTION : " + input_question + "\n\n<br><br><br>SUGGESTION QUESTIONS : <br><br>\n")
		
		for i in range(min(len(list_of_questions),number_to_display)):
		
			if(type(list_of_questions[i].link) != str or list_of_questions[i].link == "" or list_of_questions[i].link == "blank"):
		
				list_of_questions[i].link = "https://duckduckgo.com/?q=" + "+".join(list_of_questions[i].question.translate(str.maketrans('', '', string.punctuation)).split(" "))
			
			fileobj.write("\n<a href = " + "\"" + list_of_questions[i].link + "\">" + list_of_questions[i].question + "</a>" + "<br>")
			
		fileobj.write("\n\n</body>\n</html>")
		fileobj.close()
		
	except Exception as e: 
		
		print(e)
		print(type(list_of_questions[i].link))
		if(create_log_data):
			logger.info("Unable to open file : " + html_file)
			
			
