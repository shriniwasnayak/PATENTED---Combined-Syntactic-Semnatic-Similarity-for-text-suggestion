"""
Author : Shriniwas Nayak

Date : 18th Feb 2020
"""


import logging
import os
import warnings
import pandas as pd

from uiquestionclass import Questionclass
from uifileclass import FileClass
from uisyntactic import *
from uisemantic import *
from uiutility import *


#Global declarations
warnings.filterwarnings("ignore")

# forward slash '/' for linux, backward slash '\' for windows, use '\\' (since \ is special character)
filenaming = "/"
clear_command = "clear"

create_log_data = False
create_json = False
create_graph = False
create_html = True

html_file = "/home/shriniwas/BE/BEProj/UI/ProductUI/output/driver.html"
stopwords_file = "/home/shriniwas/BE/BEProj/UI/ProductUI/input/stopwords.txt"
log_file = "/home/shriniwas/BE/BEProj/UI/ProductUI/output/log.txt"
json_file = "/home/shriniwas/BE/BEProj/UI/ProductUI/output/output.json"
driver_filename = "/home/shriniwas/BE/BEProj/UI/ProductUI/input/fileinfo.txt"


number_to_display = 5


logging.basicConfig( filename = log_file , format = "%(asctime)s %(message)s", filemode = "a") 
logger=logging.getLogger("MAIN MODULE")   
logger.setLevel(logging.DEBUG)



"""
input :
output :
functionality :
"""
def determine_operation(file_name):

	if(create_log_data):
		logger.info("Starting determine_operation with input : " + file_name)

	fileobj = None

	try:

		fileobj = open(driver_filename,"r")
		
	except:

		error_msg = "Error in openeing file " + file_name
		
		if(create_log_data):
			logger.error(error_msg)
			
		exit(1)	

	#data from driver_file stored in this list	
	list_of_filenames_types = fileobj.readlines()

	#stores name of file as key and value => Syntactic : 1, Semantic : 0
	list_of_file = []


	for line in list_of_filenames_types:

		line = line.strip().split(" ")
		list_of_file.append(FileClass(line[0],line[0].split(filenaming)[-1],int(line[1])))


	for myfile in list_of_file:
	
		if(myfile.completefilename == file_name or myfile.shortname == file_name):
		
			if(create_log_data):
				logger.info("Completed determine_operation, file found")
		
			return myfile.completefilename,myfile.filetype
			
	print("\n\n:: " + file_name + " not present in the database" + " ::\n\n")	
	
	if(create_log_data):
		logger.info("Completed determine_operation, file not found")
		
	return -1,-1		

		

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
def displayquestions(list_of_questions,number_to_display,type_of_operation):


	if(create_log_data):
		logger.info("Starting display questions")

	print("\n\nSIMILAR QUESTIONS " + type_of_operation + "\n")
	print("===============================================================\n\n")

	for i in range(min(len(list_of_questions),number_to_display)):
		
		print("{0:.2f} :: ".format(list_of_questions[i].similarity_score) + list_of_questions[i].question+"\n\n")

			
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
			
			list_of_questions.append( Questionclass( int(dataframe.loc[i,"ID"]), dataframe.loc[i,"Title"], dataframe.loc[i,"Question"], dataframe.loc[i,"Link"] ) )
		
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

	iteration = 1
	w2v_model = None

	while(True):

		if(create_log_data):
			logger.info("Inside Main Menu")
		
		os.system(clear_command)
		file_name = input("\n\nEnter file name or press 0 to exit : ")
		
		if(file_name == "0"):
			break
		
		question_file,type_of_operation = determine_operation(file_name)
		
		
		if(type_of_operation == 1):
			
			syn_choice = "1"
			
			while(syn_choice == "1"):
		
				os.system(clear_command)
				input_question = input("\n\nEnter question : ") 
			
				list_of_questions = readdatafromdb(question_file)
				
				list_of_questions = syntactic_similarity_operation(list_of_questions,input_question,stopwords_file)
				
				displayquestions(list_of_questions,number_to_display,"(SYNTACTIC)")

				if(create_json):
					createjason(input_question,list_of_questions,json_file)
			
				if(create_graph):
					createGraph(list_of_questions,graph_file)
		
				if(create_html):
					createhtmlfile(list_of_questions,input_question,html_file,number_to_display)
					os.system("firefox " + html_file)
				
				syn_choice = input("\nPress 1 For another question , any key to exit : ")
				
		
		elif(type_of_operation == 0):
		
			if(iteration == 1):
				w2v_model = KeyedVectors.load_word2vec_format(model_path, binary=True)
		
			sem_choice = "1"
			
			while(sem_choice == "1"):
		
				os.system(clear_command)
		
				input_question = input("\n\nEnter question : ")
		
				list_of_questions = readdatafromdb(question_file)
				list_of_questions = semantic_similarity_operation(w2v_model,list_of_questions,input_question,stopwords_file)
				displayquestions(list_of_questions,number_to_display,"(SEMANTIC)")
				
				if(create_json):
				
					for question_obj in list_of_questions:
						question_obj.vector = list(question_obj.vector)
					
						for i in range(len(question_obj.vector)):
							question_obj.vector[i] = float(question_obj.vector[i])
							
					createjason(input_question,list_of_questions,json_file)
			
				if(create_graph):
					createGraph(list_of_questions,graph_file)
					
				if(create_html):
					createhtmlfile(list_of_questions,input_question,html_file,number_to_display)
					os.system("firefox " + html_file)

				iteration += 1

				sem_choice = input("\nPress 1 For another question , any key to exit : ")
				

		elif(type_of_operation == -1):
		
			input("\nPress key to continue\n")

	os.system(clear_command)

	
	if(create_log_data):
		logger.info("====================PROGRAM EXECUTION COMPLETED=====================")
		
				
