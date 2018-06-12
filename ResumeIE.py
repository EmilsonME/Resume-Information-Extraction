import sqlite3
import os
from docxbold import extractThis
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import re
from datetime import timedelta
import datetime
import calendar
import ntpath
import argparse
import sys
import string


# directory = "Resumes\\Test Data\\WD"
globalFilename = ""
email = []
# categoryList = jobs = ['web-developer', 'software-developer', 'systems-analyst', 'software-engineer']
category = " "
allSkills = [""]
expected = "Web Developer"

def addToDB(educ, experience, skills, certifications):
	# connection = sqlite3.connect('main.db')
	connection = sqlite3.connect('testdata2.db')
	global category
	global globalFilename
	global email
	global expected
	
	conn = connection.cursor()

	conn.execute('''INSERT INTO RESUME (CATEGORY, FILENAME, CONTACT_INFO, EXPECTED) \
					VALUES ( \'''' + category + '''\', \'''' +  globalFilename + '''\', \'''' +  email[0] + '''\', \'''' +  expected + '''\');
				''')
	if educ:
		for education in educ:
			school = education[1] if not re.findall(r'\d+', education[1]) else "N/A"
			# print(school)
			conn.execute('''INSERT INTO  EDUCATION(DEGREE, SCHOOL, RESUME_ID) \
							VALUES ( \'''' + education[0] + '''\',  \'''' + school + '''\',( SELECT MAX(RESUME_ID) AS LAST FROM RESUME ) );
						''')
	else:
		print("No Education Found: No info added to Education Table")
		
	
	for xp in experience:
		conn.execute('''INSERT INTO  EXPERIENCE(JOB_TITLE, DURATION, DESCRIPTION, RESUME_ID) \
						VALUES ( ?, ?, ?, ( SELECT MAX(RESUME_ID) AS LAST FROM RESUME ) )''', ( xp[0], xp[1], xp[2] ) )

	# out = open('skills(WebDev).txt', 'a')

	if skills:
		for skill in skills:

			s = "N/A" if not skill[1] else skill[1][0]

			query = "INSERT INTO  SKILLS(SKILL, YEARS_OF_XP, RESUME_ID)	VALUES (  %s,  %s, ( SELECT MAX(RESUME_ID) AS LAST FROM RESUME ) );"
			conn.execute('''INSERT INTO  SKILLS(SKILL, YEARS_OF_XP, RESUME_ID) \
							VALUES ( \'''' + skill[0] + '''\',  \'''' + s + '''\', ( SELECT MAX(RESUME_ID) AS LAST FROM RESUME ) );
						''')
	else:
		print("No SKILLS Found: No info added to SKILLS Table")
		
	# 	out.write(skill[0] + "\n")
		
	# out.close()

	if certifications:
		for cert in certifications:
			conn.execute('''INSERT INTO  CERTIFICATION(CERT_TITLE, RESUME_ID) \
							VALUES ( \'''' + cert[0] + '''\', ( SELECT MAX(RESUME_ID) AS LAST FROM RESUME ) );
						''')
	else:
		print("No CERTIFICATIONS Found: No info added to Trainings Table")
		
	
	connection.commit()
	connection.close()
	print("SUCCESSFULLY ADDED TO DATABASE")
	
	
		

def getToTalTime(line):

	pattern = r'january\s+\d{4}|febuary\s+\d{4}|march\s+\d{4}|april\s+\d{4}|may\s+\d{4}|june\s+\d{4}|july\s+\d{4}|august\s+\d{4}|september\s+\d{4}|october\s+\d{4}|november\s+\d{4}|december\s+\d{4}|\d{4}|present'
	result = re.findall(pattern,line.lower())
	now = datetime.datetime.now()
	dt = datetime.datetime
	if len(result) == 2:
		date1 = result[0].split()
		if len(date1) == 2:
			d1 = date1[0] + " 1 " +date1[1]
			time1 = dt.strptime(d1, '%B %d %Y')
		else: 
			d1 = "January 1 " + date1[0]
			time1 = dt.strptime(d1, '%B %d %Y')

		date2= result[1].split()
		if len(date2) == 2:
			d2 = date2[0] + " 1 " +date2[1]
			time2 = dt.strptime(d2, '%B %d %Y')
		elif date2[0] == "present":
			d2 =  calendar.month_name[now.month] + " " +  str(now.day) + " " + str(now.year)
			time2 = dt.strptime(d2, '%B %d %Y')
		else:
			d2 = "January 1 " + date2[0]
			time2 = dt.strptime(d2, '%B %d %Y')

		total_time_days =  time2 - time1

		year = round((total_time_days.days/365.5), 2)

	else:
		return 0

	return year

def getInfo(educ, skills, experience, certifications, additionalInfo, list2):	
	
	labelList = []
	counter = 0
	innerList = []
	flag = False
	listOfList = []
	listOfList2 = []
	listOfList3 = []
	listOfList4 = []
	list2 = [ i.split('\n')[0] for i in list2]

	if educ:
		for line in educ[:-1]:
			if (line in list2 and counter > 0) :
				listOfList.append(innerList)
				innerList = []
				innerList.append(line)

			elif line in list2 or flag:
				innerList.append(line)
				flag = True
				counter += 1

		else:
			if counter != 0:
				innerList.append(educ[-1])
				listOfList.append(innerList)

	counter = 0
	counter2 = 0
	innerList = []
	flag = False
	description = ""

	for line in experience[:-1]:

		if (line in list2 and counter > 0) :
			innerList.append(description if description != "" else "None")
			listOfList2.append(innerList)
			innerList = []
			innerList.append(line)
			description = ""
			flag = True

		elif line in list2 :
			innerList.append(line)
			counter += 1
			flag = True
		elif flag:
			months = getToTalTime(line)
			if months == 0 and counter2 < len(experience) - 1:
				months = getToTalTime(experience[counter2 + 1])

			flag = False
			innerList.append(months)
		else:
			description = description + line + "\n"

		counter2 += 1


	else:
		if flag:
			months = getToTalTime(experience[-1])
			flag = False
			innerList.append(months)
			innerList.append(description if description != "" else "None")
		else:
			description = description + experience[-1] 
			innerList.append(description if description != "" else "None")
	
		listOfList2.append(innerList)



	tempListOfList = [] if skills=="" else skills.split(',')

	innerList = []
	for x in tempListOfList:
		years = re.findall(r'(\d+)', x)
		retunVal = re.sub(r'\(.*\)|\.', '', x).strip()
		
		z = retunVal.split(' ')
		if len(z) > 5:
			listOfList3 = []
			break

		innerList.append(retunVal)
		innerList.append(years)
		listOfList3.append(innerList)
		innerList = []


	counter = 0
	innerList = []
	flag = False

	if certifications:
		for line in certifications[:-1]:
			if (line in list2 and counter > 0) :
				listOfList4.append(innerList)
				innerList = []
				innerList.append(line)

			elif line in list2 or flag:
				innerList.append(line)
				flag = True
				counter += 1

		else:
			if counter != 0:
				innerList.append(certifications[-1])
				listOfList4.append(innerList)

	additionalSkills = []
	exclude = set(string.punctuation)

	if additionalInfo:
		for line in additionalInfo:
			result = line.lower().strip().split(" ")			
			for x in result:
				x = ''.join(ch for ch in x if ch not in exclude)
				if x.strip() in allSkills:
					additionalSkills.append(x)	
					additionalSkills = list(filter(None, additionalSkills))
					if additionalSkills:
						additionalSkills.append(0)
						listOfList3.append(additionalSkills)
					
					additionalSkills = []

	
	if listOfList3:
		addToDB(listOfList, listOfList2, listOfList3, listOfList4)

	else:
		print("Incomplete Information: No skills found/REJECTED")


def extractAll(list1,list2):
	divisions = ["WORK EXPERIENCE", "EDUCATION", "SKILLS", "ADDITIONAL INFORMATION", "AWARDS", "CERTIFICATIONS/LICENSES", "SEMINARS/TRAININGS"]
	flag = False
	flag2 = False
	flag3 = False
	flag4 = False
	flag5 = False

	education = []
	experience = []
	certifications = []
	additionalInfo = []
	skills = ""
	
	for line in list1:
		
		if flag:
			if line.strip() in divisions  or line.strip().isupper():
				flag = False
			else:
				if line.strip():
					education.append(line)
		elif flag2:
			if line.strip() in divisions or line.strip().isupper():
				flag2 = False
			else:
				if line.strip():
					skills += line
		elif flag3:
			if line.strip() in divisions:
				flag3 = False
			else:
				if line.strip():
					experience.append(line)
		elif flag4:
			if line.strip() in divisions:
				flag4 = False
			else:
				if line.strip():
					certifications.append(line)
		elif flag5:
			if line.strip() in divisions:
				flag5 = False
			else:
				if line.strip():
					additionalInfo.append(line)

		pattern  = r'(indeed.com?\/[^\s]+)'

		if (line.strip() == "EDUCATION"):
			flag = True

		elif (line.strip() == "SKILLS"):
			flag2 = True

		elif (line.strip() == "WORK EXPERIENCE"):
			flag3 = True

		elif (line.strip() == "CERTIFICATIONS/LICENSES"):
			flag4 = True

		elif (line.strip() == "ADDITIONAL INFORMATION"):
			flag5 = True

		elif ("Email me on Indeed:" in line.strip()):
			global email
			email = re.findall(pattern, line.strip())
			

	if not skills or not experience:
		print("Incomplete Information: No skills or experiences found/REJECTED")
		out = open('rejected2.txt', 'a')
		out.write(globalFilename + "\n")
		out.close()
	else:
		getInfo(education, skills, experience, certifications, additionalInfo, list2)
	

def remove_non_ascii_2(text):
	return ''.join([i if ord(i) < 128 else ' ' for i in text])


def convert_pdf_to_txt(path):
	rsrcmgr = PDFResourceManager()
	retstr = StringIO()
	codec = 'utf-8'
	laparams = LAParams()
	device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
	fp = open(path, 'rb')
	interpreter = PDFPageInterpreter(rsrcmgr, device)
	password = ""
	maxpages = 0
	caching = True
	pagenos=set()

	for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
		interpreter.process_page(page)

	text = retstr.getvalue()

	fp.close()
	device.close()
	retstr.close()
	return text


def start(directory):

	global allSkills
	out = open("AllSkills.txt", 'r')
	for line in out.readlines():
		allSkills.append(line.strip().lower())

	# # filename =ntpath.basename(directory)
	# counter = 0
	# for filename in os.listdir(directory):
	# #for i in range(0,1):
	# 	try:
	# 		if filename.endswith(".pdf") and counter > -1:
	# 			global globalFilename
	# 			globalFilename = filename
	# 			print(filename)
	# 			list2 = extractThis(directory + "\\"+ filename)
	# 			text = convert_pdf_to_txt(directory + "\\"+ filename)
	# 			text = remove_non_ascii_2(text)
	# 			text = re.sub('\'', '', text)
	# 			line = ""
	# 			list1 = []
	# 			for letter in text:
	# 				if(letter != "\n"):
	# 					line +=letter
	# 				else:
	# 					list1.append(line)
	# 					line = ""
	# 			extractAll(list1,list2)

	# 		counter += 1
	# 	except Exception as e:
	# 		out = open('rejected3.txt', 'a')
	# 		out.write(globalFilename   + "\n" )
	# 		out.close()



	
	filename =ntpath.basename(directory)

	try:
		global globalFilename
		globalFilename = filename
		list2 = extractThis(directory)
		text = convert_pdf_to_txt(directory)
		text = remove_non_ascii_2(text)
		text = re.sub('\'', '', text)
		line = ""
		list1 = []
		for letter in text:
			if(letter != "\n"):
				line +=letter
			else:
				list1.append(line)
				line = ""
		extractAll(list1,list2)

	except Exception as e:
		print("There's an error in ",  e)


parser = argparse.ArgumentParser(description='ResumeIE')
parser.add_argument('--directory', action="store", dest='directory', default=0)
args = parser.parse_args()
# print(args.directory)

start(args.directory)

# start(directory)