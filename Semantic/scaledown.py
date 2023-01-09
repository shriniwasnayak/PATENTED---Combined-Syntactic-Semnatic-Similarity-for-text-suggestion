import nltk
import os
import string
import math
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

from gensim import corpora
from gensim.models import LsiModel
from gensim.models.coherencemodel import CoherenceModel 

#Global declarations
clear_command = "clear"
similarity_threshhold = 0.0
create_log_data = False
question_file = "testinputdata.csv"
stopwords_file = "stopwords.txt"


class Questionclass:

	def __init__(self,question_id,title,question):
	
		self.question_id = question_id
		self.title = title
		self.question = question
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
	
		return("\nQuestion id : {0}\nQuestion title : {1}\nQuestion : {2}\nSimilarity score : {3}\nVector : {4}".format(self.question_id,self.title,self.question,self.similarity_score,self.vector))



"""
input :
output :
functionality :
"""
def generate_stopwords_list(stopwords_file):

	stopwords_list = []

	try:
	
		fileobj = open(stopwords_file,"r")
	
	except:
	
		error_msg = "Error in openeing file " + stopwords_file
		print(error_msg)		
					
	list_of_lines = fileobj.readlines()
	stopwords_list = [x.split("\n")[0] for x in list_of_lines]
	
	return stopwords_list
	


"""
input :
output :
functionality :
"""
def caluculatesimilarity(vector_a,vector_b):

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
	
	size_of_vector = len(binary_vec_a)
	
	similarity = sum([binary_vec_a[i] * binary_vec_b[i] for i in range(size_of_vector)])
	
	suma = 0
	sumb = 0
	
	for i in range(size_of_vector):
	 
		suma += (binary_vec_a[i]**2)
		sumb += (binary_vec_b[i]**2)	
	
	if(suma == 0 or sumb == 0):
		return 0
	
	similarity /= math.sqrt(suma*sumb)
	
	
	return(similarity)


	
"""
input :
output :
functionality :
"""
def find_cosine_similarity(input_question_vector,list_of_questions):

	for question_object in list_of_questions:
	
		question_object.similarity_score = caluculatesimilarity(input_question_vector,question_object.vector)
				

	list_of_questions.sort(reverse = True)

	return list_of_questions



"""
input :
output :
functionality :
"""
def read_input():

	os.system(clear_command)
	print("\n\nEnter Question : \n\n\n")
	input_question = input()
		
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

	return 	input_question_vector,list_of_questions
	


"""
input :
output :
functionality :
"""
def displayquestions(list_of_questions,input_question):

	os.system(clear_command)

	print("\nINPUT QUERY : " + input_question)

	print("\n\nRESULTS [SYNTACTIC]\n")
	print("===============================================================\n\n")
	print("SIMILARITY SCORE  :: QUESTION\n\n")
	
	for question in list_of_questions:
	
		print("{0:.2f} :: ".format(question.similarity_score) + question.question + "\n")
	

def gen_matrix(list_of_questions):

	wordlist = []

	for question in list_of_questions:
	
		wordlist += question.vector
		
	wordlist = list(set(wordlist))
	
	sizeofwordlist = len(wordlist)
	sizeofdoc = len(list_of_questions)
	
	matrix = [[0]*sizeofdoc for i in range(sizeofwordlist)]
	
	for i in range(sizeofwordlist):
	
		for j in range(sizeofdoc):
		
			if(wordlist[i] in list_of_questions[j].vector):
			
				matrix[i][j] += 1
	
	mydict = {}
	
	i = 0
	
	for word in wordlist:
	
		mydict[i] = word
		i+=1
				
	mod = LsiModel(matrix, num_topics=3, id2word = mydict)
				
	
	
	
"""
input :
output :
functionality :
"""
def readdatafromdb(question_file):

	list_of_questions = []

	try:
	
		dataframe = pd.read_csv(question_file)
		
		for i in range(len(dataframe)):
			
			list_of_questions.append( Questionclass( int(dataframe.loc[i,"ID"]), dataframe.loc[i,"Title"], dataframe.loc[i,"Question"] ) )
		
	except:
		
		print("Unable to open file : " + question_file)	

	return(list_of_questions)
	
	
	
###########################################################################################################	
"""
MAIN
"""
if (__name__ == "__main__"):		
	
	list_of_questions = readdatafromdb(question_file) 	
	
	input_question = read_input()
	stopwords_list = generate_stopwords_list(stopwords_file)
	input_question_vector,list_of_questions = cleandata(input_question,list_of_questions,stopwords_list)
	list_of_questions = find_cosine_similarity(input_question_vector,list_of_questions)
	gen_matrix(list_of_questions)
	#displayquestions(list_of_questions,input_question)
	
