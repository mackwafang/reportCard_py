import tkinter as tk
import os
import xml.etree.ElementTree as xml
import xml.dom.minidom as dom # for human-readable xml
from tkinter import filedialog

def createErrorMessage(message,title="Error!",cmd=None):
	root = tk.Tk(className= title)
	label = tk.Label(root,text=message).pack(anchor=tk.CENTER)
	button = tk.Button(root,text="Close",command=root.destroy).pack()
	return root

def createEntryWithLabel(root, labelText, r, c):
	label = tk.Label(root,text=labelText)
	label.grid(row=r,column=c,sticky="W")
	entry = tk.Entry(root)
	entry.grid(row=r,column=c+1,sticky="E")
	return (label,entry)

class App(tk.Frame):
	classFolderLocation = None
	MIN_SCREEN_WIDTH = 640
	MIN_SCREEN_HEIGHT = 320

	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.classFolderLocation = tk.StringVar(master=master)
		self.pack()
		self.startScreen()
		
	def startScreen(self):
		self.master.geometry(f'{self.MIN_SCREEN_WIDTH}x{self.MIN_SCREEN_HEIGHT}')
		
		titleLabel= tk.Label(self.master,text="Welcome").pack()
		
		subFrame = tk.Frame(self.master,width=640,height=320)
		createClassButton = tk.Button(subFrame,text="Create Class",command=NewClassFolder).pack()
		createAssignmentButton = tk.Button(subFrame,text="Create Assignment").pack()
		
		subFrame.pack()

class NewClassFolder():
	windowClosed = False;
	
	def __init__(self):
		folder = filedialog.askdirectory()
		if type(folder) == str:
			subroot = tk.Tk(className="New Class Name")
			
			subroot.resizable(False,False)
			subroot.protocol("WM_DELETE_WINDOW",lambda: self.onDestroyNewClassWindow(subroot))
			
			dirLabel = tk.Label(subroot,text=folder).grid(row=0,column=0)
			
			subframe = tk.Frame(subroot)
			
			classNameEntry = createEntryWithLabel(subframe,"Class Name",1,0)
			numberOfStudentsEntry = createEntryWithLabel(subframe,"No. of Students",2,0)
			
			confirmButton = tk.Button(subframe,text="Create Class")
			confirmButton.bind("<Button-1>",lambda e: self.closeNewClassWindow(event=classNameEntry[1],numStudents=int(numberOfStudentsEntry[1].get()),dir=folder,parent=subroot))
			confirmButton.grid(row=10,column=0)
			
			cancelButton = tk.Button(subframe,text="Cancel",command=subroot.quit())
			cancelButton.grid(row=10,column=1)
			subframe.grid(row=1)
			
			subroot.mainloop()
			if not self.windowClosed:
				subroot.destroy()
	
	def onDestroyNewClassWindow(self,root):
		root.destroy()
		self.windowClosed = True;
		
	def initClassFiles(self,numStudents,fileDestination="."):
		xmlRoot = xml.Element("root")
		numStudentsData = xml.SubElement(xmlRoot,"number_of_students").text = str(numStudents)
		studentData = xml.SubElement(xmlRoot,"student_data")
		# write student data
		studentDataHeader = []
		for i in range(numStudents):
			header = xml.SubElement(studentData,"Student")
			dataName = [
				"first_name",
				"middle_name",
				"lastName",
				"preferred_name",
				"student_id",
				"family_id",
			]
			for j in dataName:
				xml.SubElement(header,j).text = " "
		
		tree = xml.tostring(xmlRoot)
		pretty_xml = dom.parseString(tree).toprettyxml()
		file = open(f"{fileDestination}/class_data",'w')
		file.write(pretty_xml)
		file.close()

		
	def confirmNewClass(self, className):
		return None
	
	def closeNewClassWindow(self,dir="./",numStudents=0,event=None,parent=None):
		# Create a new directory at "dir" with name given by the user
		# then destroys the windows
		if "entry" in str(event):
			if len(event.get()) != 0:
				folderLocation = dir+"/"+event.get()
				try:
					os.mkdir(folderLocation)
					if not parent == None:
						parent.quit()
					self.initClassFiles(numStudents,fileDestination=folderLocation)
				except FileExistsError:
					createErrorMessage(f"Folder <{folderLocation}> already exists")
			else:
				createErrorMessage("Folder name is empty!")

root = tk.Tk()
app = App(master=root)
app.mainloop()