"""
Author : Shriniwas Nayak

Date : 18th Feb 2020
"""
from codes import app


class FileClass:

	def __init__(self,completefilename,shortname,filetype):
	
		self.completefilename = completefilename
		self.shortname = shortname
		self.filetype = filetype
		
	def __str__(self):
	
		return "File name : {0}\nShort name : {1}\nFile type : {2}\n".format(self.completefilename,self.shortname,self.filetype)
