
import gensim
import numpy
import csv
import os
from gensim.models.keyedvectors import KeyedVectors
import numpy as np

#use clear for linux and cls for windows
clear_command = "clear"

#stores name of file which contains the questions
filename = "patentexample.csv"

class DocSim:
    def __init__(self, w2v_model, stopwords=None):
        self.w2v_model = w2v_model
        self.stopwords = stopwords if stopwords is not None else []

    def vectorize(self, doc):
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
        return vector

    def _cosine_sim(self, vecA, vecB):
        """Find the cosine similarity distance between two vectors."""
        csim = np.dot(vecA, vecB) / (np.linalg.norm(vecA) * np.linalg.norm(vecB))
        if np.isnan(np.sum(csim)):
            return 0
        return csim

    def calculate_similarity(self, source_doc, target_docs = None, threshold=0):
        """Calculates & returns similarity scores between given source document & all
        the target documents."""
        if not target_docs:
            return []

        if isinstance(target_docs, str):
            target_docs = [target_docs]

        source_vec = self.vectorize(source_doc)
        results = []
        for doc in target_docs:
            target_vec = self.vectorize(doc)
            sim_score = self._cosine_sim(source_vec, target_vec)
            if sim_score > threshold:
                results.append({"score": sim_score, "doc": doc})
            # Sort results by score in desc order
            results.sort(key=lambda k: k["score"], reverse=True)

        return results

############################################################################
#MAIN

listoflines = csv.reader(open(filename,"r"))

#creating a empty list
listofquestions = []

for line in listoflines:

	#index of question is 2
	listofquestions.append(line[2])
	

#deleting title "Questions" from the list	
del listofquestions[0]

model_path = 'GoogleNews-vectors-negative300.bin'

w2v_model = KeyedVectors.load_word2vec_format(model_path, binary=True)

ds = DocSim(w2v_model)

choice = "1"

while(choice == "1"):

	os.system(clear_command)
	query = input("\nEnter your question : \n\n")

	sim_scores = ds.calculate_similarity(query, listofquestions)

	#Printing results

	os.system(clear_command)
	
	print("\nINPUT QUERY : " + query)
	
	print("\n\nRESULTS [SEMANTIC]\n")
	print("===============================================================\n\n")
	print("SIMILARITY SCORE  :: QUESTION\n\n")

	for temp_dict in sim_scores:

	  print("{0:.2f} :: ".format(temp_dict["score"]) + temp_dict["doc"] + "\n")  

	choice = input("\n\nPress 1 for another question : ")
	
os.system(clear_command) 
