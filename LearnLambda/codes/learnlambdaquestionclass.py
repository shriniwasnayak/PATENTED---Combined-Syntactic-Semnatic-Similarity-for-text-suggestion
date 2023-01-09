"""
Author : Shriniwas Nayak

Date : 14th March 2020
"""


class Questionclass:

	def __init__(self,index,question_id,title,question,rank):
	
		self.index = index
		self.question_id = question_id
		self.title = title
		self.question = question
		self.rank = rank
		self.similarity_score = 0
		self.vector = None
		
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
	
		return("\nIndex : {5}\nQuestion id : {0}\nQuestion title : {1}\nQuestion : {2}\nSimilarity score : {3}\nVector : {4}\nRank : {6}".format(self.question_id,self.title,self.question,self.similarity_score,self.vector,self.index,self.rank))
