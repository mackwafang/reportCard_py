import tkinter as tk
import os
from tkinter import filedialog

def createErrorMessage(message,title="Error!",cmd=None):
	root = tk.Tk(className= title)
	label = tk.Label(root,text=message).pack(anchor=tk.CENTER)
	button = tk.Button(root,text="Close",command=root.destroy).pack()
	return root

class App(tk.Frame):
	widgetList = []
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
		self.widgetList.append(titleLabel)
		
		subFrame = tk.Frame(self.master,width=640,height=320)
		createClassButton = tk.Button(subFrame,text="Create Class",command=self.createNewClass).pack()
		self.widgetList.append(createClassButton)
		
		createAssignmentButton = tk.Button(subFrame,text="Create Assignment").pack()
		self.widgetList.append(createAssignmentButton)
		subFrame.pack()
		
		self.widgetList.append(subFrame)
		
	def createNewClass(self):
		folder = filedialog.askdirectory()
		subroot = tk.Tk(className="New Class Name")
		subroot.protocol("WM_DELETE_WINDOW",lambda: self.onDestroyNewClassWindow(subroot))
		
		dirLabel = tk.Label(subroot,text=folder).pack()
		
		subframe = tk.Frame(subroot)
		label = tk.Label(subframe,text="Folder Name:").pack(side=tk.LEFT)
		entry = tk.Entry(subframe)
		entry.bind("<Return>",lambda e: self.closeNewClassWindow(event=entry,dir=folder,parent=subroot))
		entry.pack(side=tk.LEFT)
		
		confirmButton = tk.Button(subframe,text="Create Class")
		confirmButton.bind("<Button-1>",lambda e: self.closeNewClassWindow(event=entry,dir=folder,parent=subroot))
		confirmButton.pack()
		
		subframe.pack()
		subroot.mainloop()
		subroot.destroy()
	
	def onDestroyNewClassWindow(self,root):
		root.destroy()
	
	def closeNewClassWindow(self,dir="./",event=None,parent=None):
		if "entry" in str(event):
			folderLocation = dir+"/"+event.get()
			try:
				os.mkdir(folderLocation)
				if not parent == None:
					parent.quit()
				createErrorMessage(f'Folder <{event.get()}> created at <{dir}>',title="New Folder")
			except FileExistsError:
				# print("dir exists")
				createErrorMessage(f"Folder <{folderLocation}> already exists")
root = tk.Tk()
app = App(master=root)
app.mainloop()