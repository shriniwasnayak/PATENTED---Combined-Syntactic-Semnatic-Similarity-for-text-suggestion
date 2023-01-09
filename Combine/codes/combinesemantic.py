"""
Author : Shriniwas Nayak

Date : 19th Feb 2020
"""



import logging
import os
import gensim
import numpy
import csv
import os
from gensim.models.keyedvectors import KeyedVectors
import numpy as np

from combineutility import *
from combinequestionclass import Questionclass


#Global declarations
log_file = "/home/shriniwas/BE/BEProj/Combine/output/log.txt"
stopwords_file = "/home/shriniwas/BE/BEProj/Combine/input/stopwords.txt"
model_path = '/home/shriniwas/BE/BEProj/Combine/input/GoogleNews-vectors-negative300.bin'

create_log_data = True

logging.basicConfig( filename = log_file , format = "%(asctime)s %(message)s", filemode = "a") 
logger=logging.getLogger("semantic module")   
logger.setLevel(logging.DEBUG)


class DocSim:

	def __init__(self, w2v_model, stopwords=None):

		if(create_log_data):
			logger.info("Starting initalizing DocSim")

		self.w2v_model = w2v_model
		self.stopwords = stopwords if stopwords is not None else []

		if(create_log_data):
			logger.info("Completed initalizing DocSim")

	def vectorize(self, doc):

		if(create_log_data):
			logger.info("Starting vectorize")
		

		"""Identify the vector values for each word in the given document"""
		doc = doc.lower()
		words = [w for w in doc.split(" ") if w not in self.stopwords]
		word_vecs = []

		for word in words:

			try:

				vec = self.w2v_model[word]
				word_vecs.append(vec)

			except KeyError:

				# Ignore, if the word doesn't exist in the vocabulary
				pass

		# Assuming that document vector is the mean of all the word vectors
		vector = np.mean(word_vecs, axis=0)

		if(create_log_data):
			logger.info("Completed Vectorize")

		return vector

	def _cosine_sim(self, vecA, vecB):

		if(create_log_data):
			logger.info("Strating _cosine_sim")

		#find the cosine similarity distance between two vectors.
		csim = np.dot(vecA, vecB) / (np.linalg.norm(vecA) * np.linalg.norm(vecB))

		if np.isnan(np.sum(csim)):

			return 0

		if(create_log_data):
			logger.info("Completed _cosine_sim")

		return csim

	def calculate_similarity(self, input_question, list_of_questions = None):

		if(create_log_data):
			logger.info("Starting calculate_similarity")

		#Calculates & returns similarity scores between given source document & all the target documents.

		if not list_of_questions:

			if(create_log_data):
				logger.info("list_of_questions is empty")

			return []

		source_vec = self.vectorize(input_question)
		
		for questionobj in list_of_questions:

			questionobj.vector = self.vectorize(questionobj.question)
			questionobj.similarity_score = float(self._cosine_sim(source_vec, questionobj.vector))

		list_of_questions.sort(reverse = True)

		if(create_log_data):
			logger.info("Completed calculate_similarity")

		return list_of_questions


def semantic_similarity_operation(w2v_model,list_of_questions,input_question,stopwords_file):

	if(create_log_data):
		logger.info("Starting semantic_similarity_operation")

	if(create_log_data):
		logger.info("Loading Model")
	
	stopwords_list = generate_stopwords_list(stopwords_file)
	ds = DocSim(w2v_model,stopwords_list)
	list_of_questions = ds.calculate_similarity(input_question, list_of_questions)
	
	if(create_log_data):
		logger.info("Completed semantic_similarity_operation")
	
	return list_of_questions
	
