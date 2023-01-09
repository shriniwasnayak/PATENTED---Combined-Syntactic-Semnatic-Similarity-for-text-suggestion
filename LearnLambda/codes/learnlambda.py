"""
Author : Shriniwas Nayak

Date : 14th March, 15th March 2020
"""


import logging
import os
import sys
import warnings
import pandas as pd
import copy
import numpy as np

from learnlambdaquestionclass import Questionclass
from learnlambdafileclass import FileClass
from learnlambdalambdaclass import LambdaClass
from learnlambdasyntactic import *
from learnlambdasemantic import *
from learnlambdautility import *


#Global declarations
warnings.filterwarnings("ignore")

# forward slash '/' for linux, backward slash '\' for windows, use '\\' (since \ is special character)
filenaming = "/"
clear_command = "clear"

create_log_data = True
create_json = False
create_graph = True

stopwords_file = "/home/shriniwas/BE/BEProj/LearnLambda/input/stopwords.txt"
log_file = "/home/shriniwas/BE/BEProj/LearnLambda/output/log.txt"
json_file = "/home/shriniwas/BE/BEProj/LearnLambda/output/output.json"
graphfile_path = "/home/shriniwas/BE/BEProj/LearnLambda/output/"
driver_filename = "/home/shriniwas/BE/BEProj/LearnLambda/input/covid_driverfile.txt"
observation_filename = "/home/shriniwas/BE/BEProj/LearnLambda/output/observationfile.txt"


step_increase_lambda = 0.1


logging.basicConfig( filename = log_file , format = "%(asctime)s %(message)s", filemode = "a") 
logger=logging.getLogger("MAIN MODULE")   
logger.setLevel(logging.DEBUG)



"""
input : name of question file (type : string)
output : list of questions (type : list of objects of class Question Class)
functionality : reads data from csv and appends object for each row in a list
"""
def readdatafromdb(question_file):

	list_of_questions = []

	if(create_log_data):
		logger.info("Starting readdatafromdb")

	rankindex_list = []

	try:
	
		dataframe = pd.read_csv(question_file)
		
		for i in range(len(dataframe)):
			
			list_of_questions.append( Questionclass( i, int(dataframe.loc[i,"ID"]), dataframe.loc[i,"Title"], dataframe.loc[i,"Question"], dataframe.loc[i,"Rank"] ) )
		
			if not (dataframe.loc[i,"Rank"] == None or dataframe.loc[i,"Rank"] == "" or dataframe.loc[i,"Rank"] == "blank" or numpy.isnan(dataframe.loc[i,"Rank"])):
		
				rankindex_list.append(i)
		
	except:
		
		if(create_log_data):
			logger.info("Unable to open/read file : " + question_file)
			
		exit(1)		


	if(create_log_data):
		logger.info("Completed readdatafromdb")

	return list_of_questions,rankindex_list



"""
input : name of driver file (type : string)
output : list of filename and question (type : list of FileClass Objects)
functionality : reads the driver file and creates File Class obj, 2 rows read for 1 obj creation
"""
def read_driver_file(driver_filename):

	global filenaming

	if(create_log_data):
		logger.info("Starting driver_filename")

	file_obj = None

	try:
	
		file_obj = open(driver_filename,"r")
	
	except:
		
		if(create_log_data):
			logger.info("Unable to open file : " + driver_filename)
			
		exit(1)
		
	list_of_lines = file_obj.readlines()
	
	list_of_FileClassobj = []	
	
	for iteration in range(0,len(list_of_lines)-1,2):
	
		completefilename = list_of_lines[iteration+1].strip()
	
		shortname = completefilename.split(filenaming)[-1]
	
		query_question = list_of_lines[iteration]
	
		list_of_FileClassobj.append(FileClass(completefilename,shortname,query_question))
	
		
	return list_of_FileClassobj
	


"""
input :
output :
functionality :
"""
def create_combine_list(list_of_questions_syn,list_of_questions_sem):

	
	if(create_log_data):
		logger.info("Starting create_combine_list")
	
	combine_list_of_questions = [None for iterator in range(len(list_of_questions_syn))]
		
	for question_obj in list_of_questions_syn:
	
		combine_list_of_questions[question_obj.index] = LambdaClass(question_obj.index,question_obj.question_id,question_obj.title,question_obj.question)
		combine_list_of_questions[question_obj.index].similarity_score_syn = question_obj.similarity_score 
		
	for question_obj in list_of_questions_sem:
	
		combine_list_of_questions[question_obj.index].similarity_score_sem = float(question_obj.similarity_score)			

	if(create_log_data):
		logger.info("Completed create_combine_list")
		
	return combine_list_of_questions



"""
input :
output :
functionality :
"""
def find_combine_similarity(L,combine_list_of_questions):

	if(create_log_data):
		logger.info("Starting find_combine_similarity")
	
	for obj in combine_list_of_questions:
	
		obj.similarity_score_combine = ( L * obj.similarity_score_syn ) + ( (1 - L) * obj.similarity_score_sem )
			
	combine_list_of_questions.sort(reverse = True)
	
	current_rank = 1
	
	temp_similarity_score = combine_list_of_questions[0].similarity_score_combine
	
	for obj in combine_list_of_questions:
	
		if(obj.similarity_score_combine < temp_similarity_score):
			temp_similarity_score = obj.similarity_score_combine
			current_rank += 1
	
		obj.rank = current_rank
	
	if(create_log_data):
		logger.info("Completed find_combine_similarity")

	return combine_list_of_questions




"""NOTE : in the function find_combine_similarity the combine list is sorted hence the index attribute ceases to provide serial order, hence in the function find_srds it is necessary to traverse the complete list and check if rank of that object is to be calculated using the rankindex_list"""



"""
input :
output :
functionality :
"""
def find_srds(combine_list_of_questions,rankindex_list,list_of_questions_syn):

	if(create_log_data):
		logger.info("Starting find_srds")
		
	srds = 0	
			
	for obj in combine_list_of_questions:
	
		if(obj.index in rankindex_list):

			for idobj in list_of_questions_syn:
			
				if(obj.index == idobj.index):
	
					"""print("Combine")
					print(obj)
					print("Syn")
					print(idobj)
	
					b = input("Press")"""
	
					srds += (obj.rank - idobj.rank) ** 2

	if(create_log_data):
		logger.info("Completed find_srds")
		
	return srds



"""
input :
output :
functionality :
"""
def find_avg_lambda(list_of_FileClassobj,w2v_model,observation_filename,step_increase_lambda,stopwords_file):

	if(create_log_data):
		logger.info("Starting find_avg_lambda")
	
	size = len(list_of_FileClassobj)
	
	try:
		observation_fileobj = open(observation_filename,"w")
		
	except:
	
		if(create_log_data):
			logger.info("Unable to open file : " + observation_filename)
			
		exit(1)
	
	avg_lambda = 0
	
	for obj in list_of_FileClassobj:
	
		L = 0
	
		observation_fileobj.write("==================================================\n\n")
		observation_fileobj.write("File name : " + obj.shortname + "\n")
		observation_fileobj.write("Query : " + obj.query_question + "\n\n\n")
	
		input_question = obj.query_question
	
		list_of_questions_syn,rankindex_list = readdatafromdb(obj.completefilename)		
		list_of_questions_sem = copy.deepcopy(list_of_questions_syn)
		list_of_questions_syn = syntactic_similarity_operation(list_of_questions_syn,input_question,stopwords_file)
		list_of_questions_sem = semantic_similarity_operation(w2v_model,list_of_questions_sem,input_question,stopwords_file)
		
		"""for tobj in list_of_questions_syn:
		
			print(tobj)
			
		for tobj in list_of_questions_sem:
		
			print(tobj)
			
		b = input("Press")"""
		
		combine_list_of_questions = create_combine_list(list_of_questions_syn,list_of_questions_sem)		
		
		least_srds = sys.maxsize
		best_lambda = 0
	
		Llist = []
		srdslist = []
	
		#use arange for float increment
		for L in np.arange(0.0 , 1 + step_increase_lambda , step_increase_lambda):
		
			L = float(L)
		
			if(L>1.0):
				break
		
			combine_list_of_questions = find_combine_similarity(L,combine_list_of_questions)
			
			"""for tobj in combine_list_of_questions:
			
				print(tobj)
				
			b = input("Press")"""	
			
			srds = find_srds(combine_list_of_questions,rankindex_list,list_of_questions_syn)
			
			Llist.append(L)
			srdslist.append(srds)
			
			if(srds < least_srds):
			
				least_srds = srds
				best_lambda = L
			
			observation_fileobj.write("L : {0:.3f}\tSRDS : {1}\n".format(L,srds))
			
		avg_lambda += best_lambda
	
		observation_fileobj.write("\n\n:::::::::::: BEST VALUE OF L : {0:.3f}".format(best_lambda))
		observation_fileobj.write("\n\n==================================================\n\n")	
		
		if(create_graph):
		
			#call to defined utility function
			createGraph(Llist,srdslist,graphfile_path + obj.shortname.split(".")[0] + "graph.png")
	
	avg_lambda /= size
	
	observation_fileobj.write("USE LAMBDA : {0}".format(avg_lambda))
	
	if(create_log_data):
		logger.info("Completed find_avg_lambda")
	
	return (avg_lambda)



###########################################################################################################	


"""
MAIN
"""


if (__name__ == "__main__"):		

	
	if(create_log_data):
		logger.info("=========================Starting MAIN===============================")


	list_of_FileClassobj = read_driver_file(driver_filename)

	#Learining model, takes around 1 min 10 sec
	w2v_model = KeyedVectors.load_word2vec_format(model_path, binary=True)
	#w2v_model = None
	
	L = find_avg_lambda(list_of_FileClassobj,w2v_model,observation_filename,step_increase_lambda,stopwords_file)
	
	#os.system(clear_command)
	
	print("\n\n===========================================================================")
	print("\t\t\tValue of Lambda : {0:.3f}".format(L))
	print("\n\n===========================================================================")


	if(create_log_data):
		logger.info("====================PROGRAM EXECUTION COMPLETED=====================")		
		
