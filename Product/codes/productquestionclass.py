"""
Author : Shriniwas Nayak

Date : 18th Feb 2020
"""


class Questionclass:

	def __init__(self,question_id,title,question):
	
		self.question_id = question_id
		self.title = title
		self.question = question
		self.similarity_score = 0
		self.vector = None
		
	def __lt__(self,question_obj):
	
		if(self.similarity_score < question_obj.similarity_score):	
			return True
			
		else:
			return False
		
	def __gt__(self,question_obj):
	
		if(self.similarity_score > question_obj.similarity_score):	
			return True
			
		else:
			return False


	def __eq__(self,question_obj):
	
		if(self.similarity_score == question_obj.similarity_score):	
			return True
			
		else:
			return False

	def __str__(self):
	
		return("\nQuestion id : {0}\nQuestion title : {1}\nQuestion : {2}\nSimilarity score : {3}\nVector : {4}".format(self.question_id,self.title,self.question,self.similarity_score,self.vector))
