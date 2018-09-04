#!/usr/bin/env python

import os, datetime

numberOfStudents = 0
assignmentType = ""
assignmentName = ""
maxPoints = 0
assignedDate = ""
dueDate = ""
fileName = ""
filePath = ""

def setNumberOfStudents():
	global numberOfStudents
	try:
		file = open("../studentData.csv",'r',encoding='utf-8')
		numberOfStudents -= 1
		while not file.readline() == '':
			numberOfStudents += 1
	except IOError:
		numberOfStudents = int(input("Number of Students: "))
		return
	
def setAssignmentType():
	global assignmentType
	print("<1> for HOMEWORK, <2> for PROJECT, <3> EXAM, <4> QUIZ, <5> EXTRA CREDIT.")
	t = str(input("Assignment Type: "))
	assignmentType = {
		"1":"HOMEWORK",
		"2":"PROJECT",
		"3":"EXAM",
		"4":"QUIZ",
		"5":"EXTRACREDIT",
	}.get(t,t)

def setAssignmentName():
	global assignmentName
	assignmentName = input("Assignment Name: ")

def setMaxPoints():
	global maxPoints
	maxPoints = int(input("Max Points: "))

def setAssignedDate():
	global assignedDate
	assignedDate = str(input("Assigned Date MM/DD/YYYY(use -1 for today's date): "))
	if assignedDate == "-1":
		assignedDate = str(datetime.date.today())

def setDueDate():
	global dueDate
	dueDate = str(input("Due Date MM/DD/YYYY(use -1 for today's date): "))
	if dueDate == "-1":
		dueDate = str(datetime.date.today())

def askConfirmation():
	confirmCorrect = str(input("\nAre these information correct?\n"+
							   "<1> Number of students: "+str(numberOfStudents)+"\n"+
							   "<2> Assignment type: "+assignmentType+"\n"+
				   "<3> Assignment name: "+assignmentName+"\n"+
				   "<4> Assigned date: "+assignedDate+"\n"+
				   "<5> Due date: "+dueDate+"\n"+
				   "<6> Max points: "+str(maxPoints)+"\n\n"+
				   "If so, press <Enter>. If not, press the number that corresspond with the incorrect information.\n>"))
	if len(confirmCorrect) == 0:
		global fileName
		fileName = assignmentType+"_"+assignmentName.replace(' ','_')+".csv"
		global filePath
		filePath = "../Assignments/"+fileName
		dupCount = 0;

		if not os.path.isdir("../Assignments"):
			os.mkdir("../Assignments")
		
		while os.path.isfile(filePath):
			dupCount += 1
			print(dupCount)
			fileName = assignmentType+"_"+assignmentName.replace(' ','_')+"("+str(dupCount)+").csv"
			filePath = "../Assignments/"+fileName

		file = open(filePath,"w")
		file.write("numStudents,"+str(numberOfStudents)+"\n")
		file.write("assignType,"+assignmentType+"\n")
		file.write("assignName,"+assignmentName+"\n")
		file.write("assignedDate,"+assignedDate+"\n")
		file.write("dueDate,"+dueDate+"\n")
		file.write("maxPoints,"+str(maxPoints)+"\n\n")
		file.write("CLASS_ID,SUBMIT_DATE,SCORE,NOTE\n")
		for x in range(numberOfStudents):
			file.write(str(x+1)+",,,\n")
		file.close()
	else:
		choice = {
		"1": setNumberOfStudents,
		"2": setAssignmentType,
		"3": setAssignmentName,
		"4": setAssignedDate,
		"5": setDueDate,
		"6": setMaxPoints
	}.get(confirmCorrect)
		choice()
		askConfirmation()
	
def main():
	setNumberOfStudents()
	setAssignmentType()
	setAssignmentName()
	setAssignedDate()
	setDueDate()
	setMaxPoints()

	askConfirmation()
	
	global fileName
	global filePath
	print("\""+fileName+"\" is created at \""+filePath+"\"")
main()
