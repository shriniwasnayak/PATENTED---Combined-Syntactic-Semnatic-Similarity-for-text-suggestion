"""
Author : Shriniwas Nayak

Date : 19th Feb 2020
"""



class FileClass:

	def __init__(self,completefilename,shortname,filetype):
	
		self.completefilename = completefilename
		self.shortname = shortname
		self.filetype = filetype
		
	def __str__(self):
	
		return "File name : {0}\nShort name : {1}\nFile type : {2}\n".format(self.completefilename,self.shortname,self.filetype)
