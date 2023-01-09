import csv

obj = csv.reader(open("Questions.csv","r",encoding='utf-8'))

wobj = csv.writer(open("mamadataset.csv","w"))

wobj.writerow(["ID","Title","Question"])

i = 0

for line in obj:

	if(i == 0):
		i+=1
		continue

	myline = [line[0],line[1],line[4]]
		
	wobj.writerow(myline)	
		
	i+=1
	
	if(i == 26749):
		break
