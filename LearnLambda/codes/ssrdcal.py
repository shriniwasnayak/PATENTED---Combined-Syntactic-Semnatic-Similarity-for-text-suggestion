import random

start = 1
end = 20

ssrd = 0

mylist = [4,2,1,4]

for i in mylist:

	ssrd += ((i - random.randint(1,20))**2)
	
print(ssrd)
