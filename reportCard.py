#!/usr/bin/env python
#-*- coding: utf-8 -*-

#This python file encodes in UTF-8
import os, subprocess, datetime
import Assignment
import Student

homeworks = []
projects = []
exams = []
quizes = []
extraCredits = []
studentData = []

def getLetterGrade(grade):
	if grade >= 0.93:
		return 'A'
	elif grade >= 0.90:
		return 'A-'
	elif grade >= 0.86:
		return 'B+'
	elif grade >=  0.84:
		return 'B'
	elif grade >=  0.80:
		return 'B-'
	elif grade >=  0.76:
		return 'C+'
	elif grade >=  0.74:
		return 'C'
	elif grade >=  0.70:
		return 'C-'
	elif grade >=  0.66:
		return 'D+'
	elif grade >=  0.60:
		return 'D'
	else:
		return 'F'

def getAllAssignments(s):
	# 
	# Find all files in the Assignment folder for the <s> tag, reads its content and return an array with assignment data
	#
	# Return:
	# array of all files' data or None if <Assignments> does not exists
	#
	dir = "../Assignments"
	assignments = []
	if (type(s) is not str):
		return None
	if os.path.isdir(dir):
		# list file names in the assignment folder
		files = os.listdir(dir)
		for f in files:
			# looking for homework files
			if s in f:
				openedFile = open(dir+"/"+f,"r")
				#reading content
				numStudents = int(openedFile.readline().split(',')[1])
				assignmentType = openedFile.readline().split(',')[1]
				assignmentName = openedFile.readline().split(',')[1]
				assignedDate = openedFile.readline().split(',')[1]
				dueDate = openedFile.readline().split(',')[1]
				maxPoints = openedFile.readline().split(',')[1]
				studentScoreData = []

				openedFile.readline()
				openedFile.readline()
				for x in range(0,numStudents):
					studentScoreData.append(openedFile.readline()[:-1])
				
				openedFile.close()
				a = Assignment.Assignment(assignmentType,assignmentName,assignedDate,dueDate,maxPoints,studentScoreData)
				assignments.append(a)
		return assignments
	else:
		print("<Assignments> folder does not exists")
		return None

def getStudentData():
	studentData = []
	try:
		file = open("../studentData.csv",'r',encoding='utf-8')
	except IOError:
		print("<studentData.csv> file does not exists or unreadable")
		return None

	file.readline()
	while True:
		data = file.readline().split(',')
		if len(data) != 1:
			classId = int(data[0])
			studentId = int(data[1])
			familyId = int(data[2])
			lastName = data[3]
			middleName = data[4]
			firstName = data[5]
			totalScore = int(data[6])
			percent = int(data[7])
			grade = data[8][:-1]

			s_data = Student.Student(classId,studentId,familyId,lastName,middleName,firstName,totalScore,percent,grade)
			studentData.append(s_data)
		else:
			break
		
	file.close()
	return studentData

def createReportCard():
	try:
		texFile = open("../reportCard.tex","w",encoding='utf-8')
	except IOError:
		print("<reportCard.tex> cannot be opened for writing")
		return None
	texFile.write(r"""\documentclass{article}
\usepackage[T1]{fontenc}
\usepackage[ttdefault=true]{AnonymousPro}
\renewcommand*\familydefault{\ttdefault} %% Only if the base font of the document is to be typewriter style
\usepackage{fullpage}
\usepackage{tabularx}
\usepackage[table]{xcolor}
\pagenumbering{gobble}

\begin{document}""")
	global studentData
	for student in studentData:
		print("Writing report card for "+student.lastName+", "+student.middleName+", "+student.firstName)
		texFile.write(r"""
	\begin{center}
		\begin{tabularx}{\textwidth}{X r}
			5B VN Annual Report Card & Report Compiled on """+str(datetime.date.today())+"""\\\\
			STUDENT NAME: """+student.lastName+""", """+student.middleName+""", """+student.firstName+""" & STUDENT ID: """+str(student.studentId)+"""
		\end{tabularx}
	\end{center}
	\\noindent\\rule[0.5ex]{\linewidth}{1pt}
""")
		if not homeworks == []:
			texFile.write(r"""
	\textbf{Assignments}
	\begin{center}
		\rowcolors{2}{white}{gray!25}
		\begin{tabularx}{\textwidth}{X | c | c | c | c | c}
			Name & Assigned Date & Due Date & Submit Date & Score & Grade\\
			\hline
""")
			total = 0
			maxTotal = 0
			for h in homeworks:
				parsedData = h.studentScoreData[student.classId-1].split(',')
				studentScore = parsedData[2]
				submitDate = parsedData[1]
				if len(studentScore) == 0:
					studentScore = "0"
				total += float(studentScore)
				maxTotal += int(h.maxPoints)
				texFile.write("\t\t\t"+h.assignmentName+" & "+h.assignedDate+" & "+h.dueDate+" & "+submitDate+" & " +studentScore+"/"+h.maxPoints+" & "+getLetterGrade(float(studentScore)/float(h.maxPoints))+"\\\\\n")
			texFile.write(r"""
			TOTAL & ---------- & ---------- & ---------- & """+str(('%f' % total).rstrip('0').rstrip('.'))+"""/"""+str(maxTotal)+""" & """+getLetterGrade(total/float(h.maxPoints))+"""\\
		\end{tabularx}
	\end{center}""")
	
		if not quizes == []:
			texFile.write(r"""
	\textbf{Quizes}
	\begin{center}
		\rowcolors{2}{white}{gray!25}
		\begin{tabularx}{\textwidth}{X | c | c | c}
			Name & Assigned date & Score & Grade\\
			\hline
""")
			total = 0
			maxTotal = 0
			for h in quizes:
				parsedData = h.studentScoreData[student.classId-1].split(',')
				studentScore = parsedData[2]
				submitDate = parsedData[1]
				if len(studentScore) == 0:
					studentScore = "0"
				total += float(studentScore)
				maxTotal += int(h.maxPoints)
				texFile.write("\t\t\t"+h.assignmentName+" & "+h.assignedDate+" & " +studentScore+"/"+h.maxPoints+" & "+getLetterGrade(float(studentScore)/float(h.maxPoints))+"\\\\\n")
			texFile.write(r"""
			TOTAL & ---------- & """+str(('%f' % total).rstrip('0').rstrip('.'))+"""/"""+str(maxTotal)+""" & """+getLetterGrade(total/maxTotal)+"""\\
		\end{tabularx}
	\end{center}""")
	
		if not exams == []:
			texFile.write(r"""
	\textbf{Exam}
	\begin{center}
		\rowcolors{2}{white}{gray!25}
		\begin{tabularx}{\textwidth}{X | c | c | c}
			Name & Assigned date & Score & Grade\\
			\hline
""")
			total = 0
			maxTotal = 0
			for h in exams:
				parsedData = h.studentScoreData[student.classId-1].split(',')
				studentScore = parsedData[2]
				submitDate = parsedData[1]
				if len(studentScore) == 0:
					studentScore = "0"
				total += float(studentScore)
				maxTotal += int(h.maxPoints)
				texFile.write("\t\t\t"+h.assignmentName+" & "+h.assignedDate+" & " +studentScore+"/"+h.maxPoints+" & "+getLetterGrade(float(studentScore)/float(h.maxPoints))+"\\\\\n")
			texFile.write(r"""
			TOTAL & ---------- & """+str(('%f' % total).rstrip('0').rstrip('.'))+"""/"""+str(maxTotal)+""" & """+getLetterGrade(total/maxTotal)+"""\\
		\end{tabularx}
	\end{center}""")
		
		texFile.write("\n\t\\newpage")
		
	texFile.write("\n\end{document}")
	texFile.close()
	return

def main():

	global studentData
	studentData = getStudentData()

	global homeworks
	homeworks = getAllAssignments("HOMEWORK")
	homeworks.sort(key=lambda s:s.assignedDate)
	
	global projects
	projects = getAllAssignments("PROJECT")
	projects.sort(key=lambda s:s.assignedDate)
	
	global exams
	exams = getAllAssignments("EXAM")
	exams.sort(key=lambda s:s.assignedDate)
	
	global quizes
	quizes = getAllAssignments("QUIZ")
	quizes.sort(key=lambda s:s.assignedDate)
	
	global extraCredits
	extraCredits = getAllAssignments("EXTRACREDIT")
	extraCredits.sort(key=lambda s:s.assignedDate)
	
	createReportCard()
	
	return 0

main()
	
	
#
# NOTE TO SELF: WHEN CREATING STUDENT DATA
# SAVE .CSV FILE AS CSV UTF-8
#
