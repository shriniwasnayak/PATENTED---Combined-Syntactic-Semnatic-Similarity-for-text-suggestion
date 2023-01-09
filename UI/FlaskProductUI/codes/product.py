from codes import app


import logging
import os
import warnings
from gensim.models.keyedvectors import KeyedVectors

from codes import productquestionclass
from codes import productfileclass
from codes import productsemantic
from codes import productsyntactic
from codes import productutility
from .productquestionclass import Questionclass
from .productfileclass import FileClass
from .productsyntactic import *
from .productsemantic import *
from .productutility import *


#Global declarations
warnings.filterwarnings("ignore")

# forward slash '/' for linux, backward slash '\' for windows, use '\\' (since \ is special character)
filenaming = "\\"
clear_command = "clear"

create_log_data = True
create_json = True
create_graph = True

stopwords_file = "/home/shriniwas/BE/BEProj/UI/FlaskProductUI/input/stopwords.txt"
log_file = "/home/shriniwas/BE/BEProj/UI/FlaskProductUI/output/log.txt"
json_file = "/home/shriniwas/BE/BEProj/UI/FlaskProductUI/output/output.json"
graph_file = "/home/shriniwas/BE/BEProj/UI/FlaskProductUI/output/similarity_graph.png"
driver_filename = "/home/shriniwas/BE/BEProj/UI/FlaskProductUI/input/fileinfo.txt"

number_to_display = 3



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
		list_of_file.append(productfileclass.FileClass(line[0],line[0].split(filenaming)[-1],int(line[1])))


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

	#os.system(clear_command)
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

	#for i in range(min(len(list_of_questions),number_to_display)):
    		
	#	print("{0:.2f} :: ".format(list_of_questions[i].similarity_score) + list_of_questions[i].question+"\n\n")
	if(create_log_data):
		logger.info("Completed display questions")

	return list_of_questions[0].question,list_of_questions[0].similarity_score,list_of_questions[1].question,list_of_questions[1].similarity_score,list_of_questions[2].question,list_of_questions[2].similarity_score



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
def maincode1(question_file)	:	

	file_name="E:\\College\\Project_BE\\Product\\input\\testinputdata.csv"
	if(create_log_data):
		logger.info("=========================Starting MAIN===============================")

	iteration = 1
	w2v_model = None

	while(True):

		if(create_log_data):
			logger.info("Inside Main Menu")
		
		#os.system(clear_command)
		#file_name = input("\n\nEnter file name or press 0 to exit : ")
		
		if(file_name == "0"):
			break
		
		question_file,type_of_operation = determine_operation(file_name)
		
		
		if(type_of_operation == 1):
			
			syn_choice = "1"
			
			while(syn_choice == "1"):
		
				#os.system(clear_command)
				input_question = input("\n\nEnter question : ") 
			
				list_of_questions = readdatafromdb(question_file)
				list_of_questions = productsyntactic.syntactic_similarity_operation(list_of_questions,input_question,stopwords_file)
				q1,s1,q2,s2,q3,s3=displayquestions(list_of_questions,number_to_display,"(SYNTACTIC)")

				if(create_json):
					createjason(input_question,list_of_questions,json_file)
			
				if(create_graph):
					createGraph(list_of_questions,graph_file)
		
				
				syn_choice = input("\nPress 1 For another question , any key to exit : ")
				
		
		elif(type_of_operation == 0):
		
			if(iteration == 1):
				w2v_model = KeyedVectors.load_word2vec_format(productsemantic.model_path, binary=True)
		
			sem_choice = "1"
			
			while(sem_choice == "1"):
		
				#os.system(clear_command)
		
				input_question = input("\n\nEnter question : ")
		
				list_of_questions = readdatafromdb(question_file)
				list_of_questions = productsemantic.semantic_similarity_operation(w2v_model,list_of_questions,input_question,stopwords_file)
				displayquestions(list_of_questions,number_to_display,"(SEMANTIC)")
				
				#if(create_json):
				
				#	for question_obj in list_of_questions:
				#		question_obj.vector = list(question_obj.vector)
					
				#		for i in range(len(question_obj.vector)):
				#			question_obj.vector[i] = float(question_obj.vector[i])
							
				#	createjason(input_question,list_of_questions,json_file)
			
				#if(create_graph):
				#	createGraph(list_of_questions,graph_file)

				iteration += 1

				sem_choice = input("\nPress 1 For another question , any key to exit : ")
				

		elif(type_of_operation == -1):
		
			input("\nPress key to continue\n")

	#os.system(clear_command)

	
	if(create_log_data):
		logger.info("====================PROGRAM EXECUTION COMPLETED=====================")
		
				
def maincode(input_question):
    
	file_name="E:\\College\\Project_BE\\Product\\input\\techminputdata.csv"
	if(create_log_data):
    		logger.info("=========================Starting Main===============================")
	iteration = 1
	w2v_model = None

	#while(True):

	if(create_log_data):
		logger.info("Inside Main Menu")
	
	#os.system(clear_command)
	#file_name = input("\n\nEnter file name or press 0 to exit : ")
	
	#if(file_name == "0"):
	#	break
	
	question_file,type_of_operation = determine_operation(file_name)
	
	
	if(type_of_operation == 1):
		
		#syn_choice = "1"
				
		#os.system(clear_command)
		#input_question = input("\n\nEnter question : ") 
	
		list_of_questions = readdatafromdb(question_file)
		list_of_questions = productsyntactic.syntactic_similarity_operation(list_of_questions,input_question,stopwords_file)
		q1,s1,q2,s2,q3,s3=displayquestions(list_of_questions,number_to_display,"(SYNTACTIC)")

		if(create_json):
			createjason(input_question,list_of_questions,json_file)
	
		if(create_graph):
			createGraph(list_of_questions,graph_file)

		
		#syn_choice = input("\nPress 1 For another question , any key to exit : ")
			
	
	elif(type_of_operation == 0):
	
		if(iteration == 1):
			w2v_model = KeyedVectors.load_word2vec_format(productsemantic.model_path, binary=True)
	
		#sem_choice = "1"
		
	
		#os.system(clear_command)

		input_question = input("\n\nEnter question : ")

		list_of_questions = readdatafromdb(question_file)
		list_of_questions = productsemantic.semantic_similarity_operation(w2v_model,list_of_questions,input_question,stopwords_file)
		q1,s1,q2,s2,q3,s3=displayquestions(list_of_questions,number_to_display,"(SEMANTIC)")
		
		if(create_json):
		
			for question_obj in list_of_questions:
				question_obj.vector = list(question_obj.vector)
			
				for i in range(len(question_obj.vector)):
					question_obj.vector[i] = float(question_obj.vector[i])
					
			createjason(input_question,list_of_questions,json_file)
	
		if(create_graph):
			createGraph(list_of_questions,graph_file)

		iteration += 1

		#sem_choice = input("\nPress 1 For another question , any key to exit : ")
			

	#elif(type_of_operation == -1):
	
		#input("\nPress key to continue\n")

	#os.system(clear_command)

	if(create_log_data):
    		logger.info("==============================PROGRAM EXECUTION COMPLETED=======================")


	return q1,s1,q2,s2,q3,s3



#if (__name__ == "__main__"):

#	question_file=""
#	maincode(question_file)
