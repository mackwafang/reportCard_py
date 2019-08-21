import tkinter as tk
import os
from tkinter import filedialog

def createErrorMessage(message,title="Error!",cmd=None):
	root = tk.Tk(className= title)
	label = tk.Label(root,text=message).pack(anchor=tk.CENTER)
	button = tk.Button(root,text="Close",command=root.destroy).pack()
	return root

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
			
			dirLabel = tk.Label(subroot,text=folder).grid(row=0)
			
			subframe = tk.Frame(subroot)
			label = tk.Label(subframe,text="Folder Name:").grid(row=0,column=0)
			entry = tk.Entry(subframe)
			entry.bind("<Return>",lambda e: self.closeNewClassWindow(event=entry,dir=folder,parent=subroot))
			entry.grid(row=0,column=1)
			
			confirmButton = tk.Button(subframe,text="Create Class")
			confirmButton.bind("<Button-1>",lambda e: self.closeNewClassWindow(event=entry,dir=folder,parent=subroot))
			confirmButton.grid(row=0,column=2)
			
			cancelButton = tk.Button(subframe,text="Cancel",command=subroot.quit()).grid(row=1,column=2)
			subframe.grid(row=1)
			
			subroot.mainloop()
			if not self.windowClosed:
				subroot.destroy()
	
	def onDestroyNewClassWindow(self,root):
		root.destroy()
		self.windowClosed = True;
	
	def closeNewClassWindow(self,dir="./",event=None,parent=None):
		# Create a new directory at "dir" with name given by the user
		# then destroys the windows
		if "entry" in str(event):
			if len(event.get()) != 0:
				folderLocation = dir+"/"+event.get()
				try:
					os.mkdir(folderLocation)
					if not parent == None:
						parent.quit()
					createErrorMessage(f'Folder <{event.get()}> created at <{dir}>',title="New Folder")
				except FileExistsError:
					# print("dir exists")
					createErrorMessage(f"Folder <{folderLocation}> already exists")
			else:
				createErrorMessage("Folder name is empty!")
				
root = tk.Tk()
app = App(master=root)
app.mainloop()