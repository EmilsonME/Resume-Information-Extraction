		
import sqlite3

connection = sqlite3.connect('Resumes\main.db')

cursor = connection.execute("SELECT RESUME_ID FROM SKILLS ")

skills = []

counter = 0
temp = []

for row in cursor:
	temp.append(row[0])
	# skills.append(row[0].strip())



from itertools import groupby

temp2 = [len(list(group)) for key, group in groupby(temp)]

print (max(temp2))

# uniqueSkills = list(set(skills))
# out = open('frequency.txt', 'a')

# for skill in uniqueSkills:
# 	out.write(skill + "\n")

# out.close()