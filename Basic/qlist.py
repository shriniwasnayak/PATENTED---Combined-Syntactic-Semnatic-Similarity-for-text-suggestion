#for reading the csv file
import csv


#stores name of file which contains the questions
filename = "inputdata.csv"

#currenlty size is 10 as per requirement, please modify if needed
sizeoflist = 10

listoflines = csv.reader(open(filename,"r"))


#creating a empty list
listofquestions = []

for line in listoflines:

	#index of question is 2
	listofquestions.append(line[2])
	

#deleting title "Questions" from the list	
del listofquestions[0]


#slicing list as per sizeoflist
listofquestions = listofquestions[:10]


"""
the required list is availabe with name listofquestions
"""

#TODO LSA
