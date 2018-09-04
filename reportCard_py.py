#!/usr/bin/env python
#-*- coding: utf-8 -*-

#This python file encodes in UTF-8
#
# NOTE TO SELF: WHEN CREATING STUDENT DATA
# SAVE .CSV FILE AS CSV UTF-8
#
import os, datetime
import sys
import Assignment
import Student

assignmentFolder = ""
studentDataFile = ""
outputName = "reportCard.tex"
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
	dir = assignmentFolder
	assignments = []
	if (type(s) is not str):
		return None
	if os.path.isdir(dir):
		# list file names in the assignment folder
		files = os.listdir(dir)
		for f in files:
			# looking for homework files
			if s in f:
				try:
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
				except IOError:
					return None
		return assignments
	else:
		return None

def getStudentData():
	studentData = []
	try:
		file = open(studentDataFile,'r',encoding='utf-8')
	except IOError:
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
		texFile = open("./"+outputName,"w",encoding='utf-8')
	except IOError:
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
		total = 0
		maxTotal = 0
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
			texFile.write(r"""\textbf{Assignments}
	\begin{center}
		\rowcolors{2}{white}{gray!25}
		\begin{tabularx}{\textwidth}{X | c | c | c | c | c}
			Name & Assigned Date & Due Date & Submit Date & Score & Grade\\
			\hline
""")
			assignmentTotal = 0
			assignmentMaxTotal = 0
			for h in homeworks:
				parsedData = h.studentScoreData[student.classId-1].split(',')
				studentScore = parsedData[2]
				submitDate = parsedData[1]
				if len(studentScore) == 0:
					studentScore = "0"
				assignmentTotal += float(studentScore)
				assignmentMaxTotal += int(h.maxPoints)
				texFile.write("\t\t\t"+h.assignmentName+" & "+h.assignedDate+" & "+h.dueDate+" & "+submitDate+" & " +studentScore+"/"+h.maxPoints+" & "+getLetterGrade(float(studentScore)/float(h.maxPoints))+"\\\\\n")
			total += assignmentTotal
			maxTotal += assignmentMaxTotal
			texFile.write(r"""
			TOTAL & ---------- & ---------- & ---------- & """+str(('%f' % assignmentTotal).rstrip('0').rstrip('.'))+"""/"""+str(assignmentMaxTotal)+""" & """+getLetterGrade(assignmentTotal/float(h.maxPoints))+"""\\
		\end{tabularx}
	\end{center}
	\\noindent\\rule[0.5ex]{\linewidth}{1pt}""")
	
		if not quizes == []:
			texFile.write(r"""
	\textbf{Quizes}
	\begin{center}
		\rowcolors{2}{white}{gray!25}
		\begin{tabularx}{\textwidth}{X | c | c | c}
			Name & Assigned date & Score & Grade\\
			\hline
""")
			assignmentTotal = 0
			assignmentMaxTotal = 0
			for h in quizes:
				parsedData = h.studentScoreData[student.classId-1].split(',')
				studentScore = parsedData[2]
				submitDate = parsedData[1]
				if len(studentScore) == 0:
					studentScore = "0"
				assignmentTotal += float(studentScore)
				assignmentMaxTotal += int(h.maxPoints)
				texFile.write("\t\t\t"+h.assignmentName+" & "+h.assignedDate+" & " +studentScore+"/"+h.maxPoints+" & "+getLetterGrade(float(studentScore)/float(h.maxPoints))+"\\\\\n")
			total += assignmentTotal
			maxTotal += assignmentMaxTotal
			texFile.write(r"""
			TOTAL & ---------- & """+str(('%f' % assignmentTotal).rstrip('0').rstrip('.'))+"""/"""+str(assignmentMaxTotal)+""" & """+getLetterGrade(assignmentTotal/assignmentMaxTotal)+"""\\
		\end{tabularx}
	\end{center}
	\\noindent\\rule[0.5ex]{\linewidth}{1pt}""")

		if not projects == []:
			texFile.write(r"""
	\textbf{Projects}
	\begin{center}
		\rowcolors{2}{white}{gray!25}
		\begin{tabularx}{\textwidth}{X | c | c | c | c | c}
			Name & Assigned Date & Due Date & Submit Date & Score & Grade\\
			\hline
""")
			assignmentTotal = 0
			assignmentMaxTotal = 0
			for h in projects:
				parsedData = h.studentScoreData[student.classId-1].split(',')
				studentScore = parsedData[2]
				submitDate = parsedData[1]
				if len(studentScore) == 0:
					studentScore = "0"
				assignmentTotal += float(studentScore)
				assignmentMaxTotal += int(h.maxPoints)
				texFile.write("\t\t\t"+h.assignmentName+" & "+h.assignedDate+" & "+h.dueDate+" & "+submitDate+" & " +studentScore+"/"+h.maxPoints+" & "+getLetterGrade(float(studentScore)/float(h.maxPoints))+"\\\\\n")
			total += assignmentTotal
			maxTotal += assignmentMaxTotal
			texFile.write(r"""
			TOTAL & ---------- & ---------- & ---------- & """+str(('%f' % assignmentTotal).rstrip('0').rstrip('.'))+"""/"""+str(assignmentMaxTotal)+""" & """+getLetterGrade(assignmentTotal/float(h.maxPoints))+"""\\
		\end{tabularx}
	\end{center}
	\\noindent\\rule[0.5ex]{\linewidth}{1pt}""")
	
		if not extraCredits == []:
			texFile.write(r"""
	\textbf{Extra Credits}
	\begin{center}
		\rowcolors{2}{white}{gray!25}
		\begin{tabularx}{\textwidth}{X | c}
			Name & Score\\
			\hline
""")
			assignmentTotal = 0
			assignmentMaxTotal = 0
			for h in extraCredits:
				parsedData = h.studentScoreData[student.classId-1].split(',')
				studentScore = parsedData[2]
				submitDate = parsedData[1]
				if len(studentScore) == 0:
					studentScore = "0"
				assignmentTotal += float(studentScore)
				assignmentMaxTotal += int(h.maxPoints)
				texFile.write("\t\t\t"+h.assignmentName+" & +" +studentScore+"/"+h.maxPoints+"\\\\\n")
			total += assignmentTotal
			texFile.write(r"""
			TOTAL & +"""+str(('%f' % assignmentTotal).rstrip('0').rstrip('.'))+"""\\
		\end{tabularx}
	\end{center}
	\\noindent\\rule[0.5ex]{\linewidth}{1pt}""")
	
		if not exams == []:
			texFile.write(r"""
	\textbf{Exam}
	\begin{center}
		\rowcolors{2}{white}{gray!25}
		\begin{tabularx}{\textwidth}{X | c | c | c}
			Name & Assigned date & Score & Grade\\
			\hline
""")
			assignmentTotal = 0
			assignmentMaxTotal = 0
			for h in exams:
				parsedData = h.studentScoreData[student.classId-1].split(',')
				studentScore = parsedData[2]
				submitDate = parsedData[1]
				if len(studentScore) == 0:
					studentScore = "0"
				assignmentTotal += float(studentScore)
				assignmentMaxTotal += int(h.maxPoints)
				texFile.write("\t\t\t"+h.assignmentName+" & "+h.assignedDate+" & " +studentScore+"/"+h.maxPoints+" & "+getLetterGrade(float(studentScore)/float(h.maxPoints))+"\\\\\n")
			total += assignmentTotal
			maxTotal += assignmentMaxTotal
			texFile.write(r"""
			TOTAL & ---------- & """+str(('%f' % assignmentTotal).rstrip('0').rstrip('.'))+"""/"""+str(assignmentMaxTotal)+""" & """+getLetterGrade(assignmentTotal/assignmentMaxTotal)+"""\\
		\end{tabularx}
	\end{center}
	\\noindent\\rule[0.5ex]{\linewidth}{1pt}""")
	
		texFile.write(r"""
		\begin{center}
			\begin{tabularx}{\textwidth}{X | c | c}
				& Score & Grade\\
				TOTAL & """+str(str(('%f' % total).rstrip('0').rstrip('.')))+"""/"""+str(maxTotal)+""" & """+getLetterGrade(total/maxTotal)+"""\\
			\end{tabularx}
		\end{center}
		""")
		texFile.write("\n\t\\newpage")
		
	texFile.write("\n\end{document}")
	texFile.close()
	return 0

def main(file,folder,name):
	
	global assignmentFolder
	assignmentFolder = folder
	
	global studentDataFile
	studentDataFile = file
	
	global outputName
	outputName = name
	
	global studentData
	studentData = getStudentData()
	if studentData == None:
		return 1
	
	global homeworks
	homeworks = getAllAssignments("HOMEWORK")
	
	global projects
	projects = getAllAssignments("PROJECT")
	
	global exams
	exams = getAllAssignments("EXAM")
	
	global quizes
	quizes = getAllAssignments("QUIZ")
	
	global extraCredits
	extraCredits = getAllAssignments("EXTRACREDIT")
	
	if homeworks == None or projects == None or exams == None or quizes == None or extraCredits == None:
		return 2
	else:
		homeworks.sort(key=lambda s:s.assignedDate)
		projects.sort(key=lambda s:s.assignedDate)
		exams.sort(key=lambda s:s.assignedDate)
		quizes.sort(key=lambda s:s.assignedDate)
		extraCredits.sort(key=lambda s:s.assignedDate)
		if createReportCard() == None:
			return 3
	
	return 0
