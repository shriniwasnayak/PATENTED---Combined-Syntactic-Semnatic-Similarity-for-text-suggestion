"""
Author : Shriniwas Nayak

Date : 19th Feb 2020
"""


class LambdaClass:

	def __init__(self,question_id,title,question):
	
		self.question_id = question_id
		self.title = title
		self.question = question
		self.similarity_score_combine = 0
		self.similarity_score_syn = 0
		self.similarity_score_sem = 0
		
	def __lt__(self,question_obj):
	
		if(self.similarity_score_combine < question_obj.similarity_score_combine):	
			return True
			
		else:
			return False
		
	def __gt__(self,question_obj):
	
		if(self.similarity_score_combine > question_obj.similarity_score_combine):	
			return True
			
		else:
			return False


	def __eq__(self,question_obj):
	
		if(self.similarity_score_combine == question_obj.similarity_score_combine):	
			return True
			
		else:
			return False

	def __str__(self):
	
		return("\nQuestion id : {0}\nQuestion title : {1}\nQuestion : {2}\nCombine Similarity score : {3}\nSyntactic Similarity score : {4}\nSemantic Similarity score : {5}".format(self.question_id,self.title,self.question,self.similarity_score_combine,self.similarity_score_syn,self.similarity_score_sem))
