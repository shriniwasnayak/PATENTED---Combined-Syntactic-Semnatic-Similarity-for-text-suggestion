"""
Author : Shriniwas Nayak

Date : 14th March 2020
"""



class FileClass:

	def __init__(self,completefilename,shortname,query_question):
	
		self.completefilename = completefilename
		self.shortname = shortname
		self.query_question = query_question
		
	def __str__(self):
	
		return "File name : {0}\nShort name : {1}\nQuery Question : {2}\n".format(self.completefilename,self.shortname,self.query_question)
