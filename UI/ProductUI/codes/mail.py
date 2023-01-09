
import smtplib 
import os

logfile_path = "/home/shriniwas/BE/BEProj/UI/ProductUI/output/"
logfile_name = "log.txt"
 
sender_email = "landdigitizationproject@gmail.com"
password = "saa414256"
 

def read_list_of_receipients():

	list_of_receipients = [address.strip() for address in input("\nEnter space separated receipent mail address : \n\n").split(" ")]	
	
	if(len(list_of_receipients) == 0):
	
		list_of_receipients = ["anujkanetkar@gmail.com", "hrushabh.hirudkar@gmail.com","shriniwasnayak1@gmail.com"] 

	return list_of_receipients



def generate_summary(logfile_path,logfile_name):

	file_obj = open(logfile_path + logfile_name)

	lines = file_obj.readlines()

	summary = ""
	errors = 0
	start_date = ""
	end_date = ""
	runs = 0
	
	for line in lines:
	
		temp = line.split(" ")
		
		if("=========================Starting" in temp):
		
			runs+=1
			
		if("Unable" in temp):
			errors+=1
			
	start_date = lines[0].split(" ")[0]
	end_date = lines[-1].split(" ")[0]

	summary += "Please find mentioned below summary report of Query suggestion System : \n\n\n"
	summary += "START DATE : {0}\n".format(start_date)
	summary += "END DATE : {0}\n".format(end_date)
	summary += "Total executions : {0}\n".format(runs)
	summary += "Total errors : {0}\n".format(errors)
	summary += "\n\nThanks & Regards"

	return summary
  


def send_mail(list_of_receipients,summary,sender_email,password):
 	
	for destination in list_of_receipients: 

		try:
		
			smtp_obj = smtplib.SMTP('smtp.gmail.com', 587) 

			smtp_obj.starttls() 

			smtp_obj.login("landdigitizationproject@gmail.com", "saa414256") 
			
			message = 'Subject: {0}\n\n{1}'.format("System Summary Report", summary)
			
			smtp_obj.sendmail("landdigitizationproject@gmail.com", destination, message) 

			smtp_obj.quit()
			
		except Exception as e:

			print(e)
		
			print("Unable to send mail to " + destination)			 

		
#main

list_of_receipients = read_list_of_receipients()
summary = generate_summary(logfile_path,logfile_name)

send_mail(list_of_receipients,summary,sender_email,password)

print("\n\n !! Mails Sent !!\n\n")


	
