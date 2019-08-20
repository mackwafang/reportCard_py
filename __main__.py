import os, sys, subprocess
import reportCard

def getHelp():
	print("--------|----------------------------------------------")
	print("Command | Purpose")
	print("--------|----------------------------------------------")
	print("create  | Create an assignment and put it in a folder\n"+
		  "        | Usage: create <Folder> <studentDataFile>")
	print("--------|----------------------------------------------")
	print("compile | Create a report card\n"+
		  "        | Usage: compile <StudentDataFile> <Folder> [outputName]")
	print("--------|----------------------------------------------")
	print("exit    | Exit this program")
	print("--------|----------------------------------------------")
	print("help    | Display this message")

if __name__ == "__main__":
	print("What would you like to do?")
	getHelp()
	
	while True:
		command = input("> ")
		arg = command.split(' ')
		if arg[0] == "create":
			if len(arg) == 3:
				subprocess.call(['python','./reportCard/createAssignmentFile.py',arg[1],arg[2]])
			else:
				print("Usage: create <Folder> <studentDataFile>")
		elif arg[0] == "compile":
			if len(arg) >= 3:
				name = "reportCard.tex"
				if len(arg) == 4:
					name = arg[3]
				else:
					name = "reportCard.tex"
				print("Compiling...")
				returnCode = reportCard.main(os.getcwd()+"/"+arg[1],os.getcwd()+"/"+arg[2]+"/",name)
				if not returnCode == 0:
					print("Error "+str(returnCode)+": "+{
						1:"Student data cannot be gathered. Please check your student data file.",
						2:"Assignment data cannot be gathered. Please check your assignment folder",
						3:"Report Card cannot be written",
					}.get(returnCode),file=sys.stderr)
				else:
					print(".tex file written")
					try:
						print("fetching xelatex...")
						process = subprocess.Popen(['xelatex',name])
						process.communicate()
						print("done")
					except CalledProcessError:
						print("xelatex error")
			else:
				print("Usage: compile <StudentDataFile> <Folder>")
		elif arg[0] == "help":
			getHelp()
		elif arg[0] == "exit":
			sys.exit()